from typing import Dict, Any, Optional


class InfrastructureException(Exception):
    """
    Classe base para exceções da camada de infraestrutura.
    
    Representa erros relacionados a recursos externos como
    banco de dados, APIs, sistemas de arquivos, etc.
    """
    
    def __init__(self, message: str, error_code: str = None, details: Optional[Dict[str, Any]] = None):
        """
        Inicializa uma exceção de infraestrutura.
        
        Args:
            message: Mensagem de erro legível
            error_code: Código único de erro
            details: Detalhes adicionais sobre o erro
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte a exceção para dicionário."""
        return {
            "error_type": self.__class__.__name__,
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details
        }


class DatabaseException(InfrastructureException):
    """
    Exceção lançada quando há problemas com o banco de dados.
    """
    
    def __init__(self, message: str, operation: str = "", table: str = "", original_exception: Exception = None):
        """
        Inicializa exceção de banco de dados.
        
        Args:
            message: Mensagem de erro
            operation: Operação que causou o erro (SELECT, INSERT, etc.)
            table: Tabela envolvida no erro
            original_exception: Exceção original do SQLAlchemy/driver
        """
        details = {
            "operation": operation,
            "table": table,
            "original_error": str(original_exception) if original_exception else None
        }
        super().__init__(
            message=message,
            error_code="DATABASE_ERROR",
            details=details
        )
        self.original_exception = original_exception


class ConnectionException(DatabaseException):
    """
    Exceção lançada quando há problemas de conexão com o banco.
    """
    
    def __init__(self, database_url: str, original_exception: Exception = None):
        """
        Inicializa exceção de conexão.
        
        Args:
            database_url: URL do banco (sem credenciais sensíveis)
            original_exception: Exceção original
        """
        # Remove credenciais da URL para logs de segurança
        safe_url = database_url.split('?')[0] if database_url else "unknown"
        
        message = f"Falha ao conectar com o banco de dados: {safe_url}"
        details = {
            "database_url": safe_url,
            "original_error": str(original_exception) if original_exception else None
        }
        
        super(InfrastructureException, self).__init__(
            message=message,
            error_code="CONNECTION_ERROR", 
            details=details
        )
        self.original_exception = original_exception


class RepositoryException(InfrastructureException):
    """
    Exceção lançada quando há problemas nos repositórios.
    """
    
    def __init__(self, repository_name: str, operation: str, entity_id: str = "", original_exception: Exception = None):
        """
        Inicializa exceção de repositório.
        
        Args:
            repository_name: Nome do repositório
            operation: Operação que falhou
            entity_id: ID da entidade (se aplicável)
            original_exception: Exceção original
        """
        message = f"Erro no {repository_name} durante {operation}"
        if entity_id:
            message += f" para entidade {entity_id}"
        
        details = {
            "repository": repository_name,
            "operation": operation,
            "entity_id": entity_id,
            "original_error": str(original_exception) if original_exception else None
        }
        
        super().__init__(
            message=message,
            error_code="REPOSITORY_ERROR",
            details=details
        )
        self.original_exception = original_exception


class MappingException(InfrastructureException):
    """
    Exceção lançada quando há problemas no mapeamento entidade/modelo.
    """
    
    def __init__(self, mapping_direction: str, entity_type: str, field_name: str = "", original_exception: Exception = None):
        """
        Inicializa exceção de mapeamento.
        
        Args:
            mapping_direction: Direção do mapeamento (to_model, to_entity)
            entity_type: Tipo da entidade sendo mapeada
            field_name: Nome do campo problemático (se específico)
            original_exception: Exceção original
        """
        message = f"Erro no mapeamento {mapping_direction} para {entity_type}"
        if field_name:
            message += f" no campo '{field_name}'"
        
        details = {
            "mapping_direction": mapping_direction,
            "entity_type": entity_type,
            "field_name": field_name,
            "original_error": str(original_exception) if original_exception else None
        }
        
        super().__init__(
            message=message,
            error_code="MAPPING_ERROR",
            details=details
        )
        self.original_exception = original_exception