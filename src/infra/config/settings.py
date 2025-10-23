from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Configurações da aplicação.
    
    Utiliza variáveis de ambiente com fallback para valores padrão.
    """
    
    
    # String de conexão SQL Server (alternativa ao database_url)
    sql_server_connection_string: Optional[str] = None
    sql_server_database_name: str = "questoes_db"

    # Configurações Azure OpenAI
    endpoint_url: Optional[str] = None
    deployment_name: Optional[str] = None
    azure_openai_api_key: Optional[str] = None

    # Configurações da API
    api_title: str = "API de chat com Clean Architecture"
    api_description: str = "API para gerenciamento de usuários usando Clean Architecture"
    api_version: str = "1.0.0"

    # Configurações do servidor
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = True
    log_level: str = "info"

    # Configurações de CORS (mais seguras por padrão)
    cors_origins: list[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
        "http://127.0.0.1:3000",
        "http://localhost:4200"
    ]
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    cors_allow_headers: list[str] = ["Accept", "Accept-Language", "Content-Language", "Content-Type", "Authorization"]

    # Configurações de paginação
    max_page_size: int = 1000
    default_page_size: int = 100

    # Configurações de monitoramento
    rollbar_access_token: Optional[str] = None
    rollbar_environment: str = "development"
    enable_rollbar: bool = False
    
    def get_database_url(self) -> str:
        """
        Retorna a URL do banco de dados, processando a string de conexão SQL Server se fornecida.
        
        Returns:
            str: URL do banco de dados para SQLAlchemy
        """
        if self.sql_server_connection_string:
            from ...interfaces.shared.utils.sql_server_helper import SqlServerConnectionHelper
            return SqlServerConnectionHelper.to_sqlalchemy_url(
                self.sql_server_connection_string, 
                self.sql_server_database_name
            )
        return self.database_url
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Instância global das configurações
settings = Settings()