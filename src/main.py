
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from src.infra.config import settings
from src.infra.applicationBdContext.database import initialize_database, get_database_config
from src.infra.services.questao_repository import QuestaoRepository
from src.application.services.questao_service import QuestaoService
from src.interfaces.api.controllers.questao_controller import router as questao_router
from src.interfaces.shared.security.rate_limiter import check_rate_limit
from src.interfaces.shared.exceptions import ExceptionHandler
import time

# Criação da aplicação FastAPI
app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    version=settings.api_version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuração do CORS centralizada
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Middleware de segurança
@app.middleware("http")
async def security_middleware(request: Request, call_next):
    await check_rate_limit(request)
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "style-src 'self' https://cdn.jsdelivr.net; "
        "script-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; "
        "img-src 'self' data: https://fastapi.tiangolo.com; "
        "connect-src 'self' https://cdn.jsdelivr.net;"
    )
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    if "Server" in response.headers:
        del response.headers["Server"]
    return response

# Configura os exception handlers
ExceptionHandler.setup_exception_handlers(app)

# Inicialização do banco e dependências
from src.application.services.openai_service import OpenAIService

def setup_dependencies():
    app.include_router(questao_router)

@app.on_event("startup")
async def startup_event():
    print("🚀 Inicializando aplicação...")
    database_url = settings.get_database_url()
    # Sanitiza URL do banco para logs
    safe_db_url = database_url.split('?')[0] if '?' in database_url else database_url
    if '@' in safe_db_url:
        parts = safe_db_url.split('@')
        if len(parts) > 1:
            protocol_and_user = parts[0].split('//')
            if len(protocol_and_user) > 1:
                safe_db_url = f"{protocol_and_user[0]}//**redacted**@{parts[1]}"
    print(f"📊 Conectando ao banco: {safe_db_url}...")
    initialize_database(database_url)
    setup_dependencies()
    # Inicializa Rollbar se habilitado
    if settings.enable_rollbar and settings.rollbar_access_token:
        try:
            import rollbar
            rollbar.init(
                access_token=settings.rollbar_access_token,
                environment=settings.rollbar_environment,
                code_version=settings.api_version
            )
            print("� Rollbar inicializado!")
            rollbar.report_message('🚀 API inicializada com sucesso!', 'info')
        except Exception as e:
            print(f"⚠️ Erro ao inicializar Rollbar: {e}")
    print("✅ Aplicação inicializada com sucesso!")

# Endpoints de saúde
@app.get("/", tags=["health"])
async def health_check():
    return {
        "status": "healthy",
        "message": "API está funcionando!",
        "version": settings.api_version,
        "docs": "/docs"
    }

@app.get("/health", tags=["health"])
async def detailed_health_check():
    try:
        db_config = get_database_config()
        session = db_config.get_session()
        session.close()
        return {
            "status": "healthy",
            "database": "connected",
            "version": settings.api_version,
            "features": {
                "questaos": "available",
                "crud_operations": "available",
                "validation": "enabled",
                "security_monitoring": settings.enable_rollbar,
                "rate_limiting": "enabled"
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "version": settings.api_version
        }

@app.get("/security/stats", tags=["security"])
async def security_stats():
    try:
        from src.interfaces.shared.security.security_monitor import security_monitor
        stats = security_monitor.get_security_stats()
        return {
            "status": "success",
            "data": stats,
            "timestamp": time.time()
        }
    except ImportError:
        return {
            "status": "error",
            "message": "Monitor de segurança não disponível",
            "basic_protection": "rate_limiting_enabled"
        }

# Removidos endpoints de teste/debug do Rollbar
