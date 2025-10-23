from typing import Dict, Any, Optional
from ....domain.exceptions.base_exception import DomainException
# from ...Domain.Exceptions.base_exception import DomainException


class ApplicationException(Exception):
    """
    Classe base para exceções da camada de aplicação.
    
    Representa erros relacionados a operações de aplicação,
    orquestração de serviços e coordenação de casos de uso.
    """
    
    def __init__(self, message: str, error_code: str = None, details: Optional[Dict[str, Any]] = None):
        """
        Inicializa uma exceção de aplicação.
        
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


class CommandValidationException(ApplicationException):
    """
    Exceção lançada quando um comando não passa na validação.
    """
    
    def __init__(self, command_type: str, validation_errors: Dict[str, str]):
        """
        Inicializa exceção de validação de comando.
        
        Args:
            command_type: Tipo do comando que falhou
            validation_errors: Dicionário com erros de validação
        """
        message = f"Erro de validação no comando {command_type}"
        details = {
            "command_type": command_type,
            "validation_errors": validation_errors
        }
        super().__init__(
            message=message,
            error_code="COMMAND_VALIDATION_ERROR",
            details=details
        )


class QueryValidationException(ApplicationException):
    """
    Exceção lançada quando uma query não passa na validação.
    """
    
    def __init__(self, query_type: str, validation_errors: Dict[str, str]):
        """
        Inicializa exceção de validação de query.
        
        Args:
            query_type: Tipo da query que falhou
            validation_errors: Dicionário com erros de validação
        """
        message = f"Erro de validação na query {query_type}"
        details = {
            "query_type": query_type,
            "validation_errors": validation_errors
        }
        super().__init__(
            message=message,
            error_code="QUERY_VALIDATION_ERROR",
            details=details
        )


class ServiceUnavailableException(ApplicationException):
    """
    Exceção lançada quando um serviço necessário não está disponível.
    """
    
    def __init__(self, service_name: str, reason: str = ""):
        """
        Inicializa exceção de serviço indisponível.
        
        Args:
            service_name: Nome do serviço indisponível
            reason: Razão da indisponibilidade
        """
        message = f"Serviço '{service_name}' não está disponível"
        if reason:
            message += f": {reason}"
        
        details = {
            "service_name": service_name,
            "reason": reason
        }
        super().__init__(
            message=message,
            error_code="SERVICE_UNAVAILABLE",
            details=details
        )


class ConcurrencyException(ApplicationException):
    """
    Exceção lançada quando há conflitos de concorrência.
    """
    
    def __init__(self, resource_type: str, resource_id: str, operation: str = ""):
        """
        Inicializa exceção de concorrência.
        
        Args:
            resource_type: Tipo do recurso em conflito
            resource_id: ID do recurso em conflito
            operation: Operação que causou o conflito
        """
        message = f"Conflito de concorrência no {resource_type} {resource_id}"
        if operation:
            message += f" durante {operation}"
        
        details = {
            "resource_type": resource_type,
            "resource_id": resource_id,
            "operation": operation
        }
        super().__init__(
            message=message,
            error_code="CONCURRENCY_CONFLICT",
            details=details
        )