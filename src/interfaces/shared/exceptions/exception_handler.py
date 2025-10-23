from fastapi import Request, HTTPException, status, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
from typing import Dict, Any

from ..exceptions.application_exceptions import (
    ApplicationException,
    DomainException
)


logger = logging.getLogger(__name__)

class ExceptionHandler:
    @staticmethod
    def create_error_reponse(
        status_code: int,
        error_type: str,
        message: str,
        details: Dict[str, Any] = None,
        request_id: str = None
    ) -> JSONResponse:
        """
        Cria uma resposta de erro padronizada.

        Args:
            status_code: Código de status HTTP
            error_type: Tipo de erro
            message: Mensagem de erro
            details: Detalhes adicionais sobre o erro
            request_id: ID da requisição (opcional)

        Returns:
            JSONResponse com a estrutura de erro padronizada
        """
        error_response = {
            "error": {
                "type": error_type,
                "message": message,
                "details": details,
                "request_id": request_id
            }
        }
        return JSONResponse(status_code=status_code, content=error_response)

    @staticmethod
    async def handle_exception(request: Request, exc: Exception) -> JSONResponse:
        """
        Manipula exceções e retorna respostas HTTP apropriadas.

        Args:
            request: Objeto de requisição FastAPI
            exc: Exceção capturada

        Returns:
            JSONResponse com a resposta de erro apropriada
        """
        request_id = request.headers.get("X-Request-ID", None)

        if isinstance(exc, StarletteHTTPException):
            return ExceptionHandler.create_error_reponse(
                status_code=exc.status_code,
                error_type="HTTPException",
                message=exc.detail,
                request_id=request_id
            )

        elif isinstance(exc, RequestValidationError):
            return ExceptionHandler.create_error_reponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                error_type="ValidationError",
                message="Erro de validação na requisição.",
                details=exc.errors(),
                request_id=request_id
            )

        elif isinstance(exc, DomainException):
            return ExceptionHandler.create_error_reponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                error_type=exc.__class__.__name__,
                message=exc.message,
                details=exc.to_dict().get("details", {}),
                request_id=request_id
            )

        elif isinstance(exc, ApplicationException):
            return ExceptionHandler.create_error_reponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_type=exc.__class__.__name__,
                message=exc.message,
                details=exc.to_dict().get("details", {}),
                request_id=request_id
            )


        else:
            logger.error(f"Unhandled exception: {str(exc)}")
            return ExceptionHandler.create_error_reponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                error_type="InternalServerError",
                message="Ocorreu um erro interno no servidor.",
                request_id=request_id
            )

    @staticmethod
    def setup_exception_handlers(app: FastAPI):
        """
        Registra handlers globais de exceção na aplicação FastAPI.
        """
        @app.exception_handler(StarletteHTTPException)
        async def http_exception_handler(request: Request, exc: StarletteHTTPException):
            return ExceptionHandler.create_error_reponse(
                status_code=exc.status_code,
                error_type="HTTPException",
                message=exc.detail,
                request_id=request.headers.get("X-Request-ID", None)
            )

        @app.exception_handler(RequestValidationError)
        async def validation_exception_handler(request: Request, exc: RequestValidationError):
            return ExceptionHandler.create_error_reponse(
                status_code=422,
                error_type="ValidationError",
                message="Erro de validação na requisição.",
                details=exc.errors(),
                request_id=request.headers.get("X-Request-ID", None)
            )

        @app.exception_handler(DomainException)
        async def domain_exception_handler(request: Request, exc: DomainException):
            return ExceptionHandler.create_error_reponse(
                status_code=400,
                error_type=exc.__class__.__name__,
                message=exc.message,
                details=exc.to_dict().get("details", {}),
                request_id=request.headers.get("X-Request-ID", None)
            )

        @app.exception_handler(ApplicationException)
        async def application_exception_handler(request: Request, exc: ApplicationException):
            return ExceptionHandler.create_error_reponse(
                status_code=500,
                error_type=exc.__class__.__name__,
                message=exc.message,
                details=exc.to_dict().get("details", {}),
                request_id=request.headers.get("X-Request-ID", None)
            )


        @app.exception_handler(Exception)
        async def generic_exception_handler(request: Request, exc: Exception):
            logging.error(f"Unhandled exception: {str(exc)}")
            return ExceptionHandler.create_error_reponse(
                status_code=500,
                error_type="InternalServerError",
                message="Ocorreu um erro interno no servidor.",
                request_id=request.headers.get("X-Request-ID", None)
            )



