from abc import ABC
from typing import Dict, Any, Optional


class DomainException(Exception, ABC):
    """
    Classe base para todas as exceções de domínio.
    
    Representa violações de regras de negócio ou invariantes do domínio.
    """
    
    def __init__(self, message: str, error_code: str = None, details: Optional[Dict[str, Any]] = None):
        """
        Inicializa uma exceção de domínio.
        
        Args:
            message: Mensagem de erro legível para humanos
            error_code: Código único de erro para identificação programática
            details: Detalhes adicionais sobre o erro
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte a exceção para um dicionário.
        
        Returns:
            Dict com informações da exceção
        """
        return {
            "error_type": self.__class__.__name__,
            "error_code": self.error_code,
            "message": self.message,
            "details": self.details
        }
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}: {self.message}"
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(message='{self.message}', error_code='{self.error_code}')"


class BusinessRuleViolationException(DomainException):
    """
    Exceção lançada quando uma regra de negócio é violada.
    """
    pass


class ValidationException(DomainException):
    """
    Exceção lançada quando dados não passam na validação de domínio.
    """
    pass


class DomainEntityNotFoundException(DomainException):
    """
    Exceção lançada quando uma entidade de domínio não é encontrada.
    """
    pass


class DomainEntityAlreadyExistsException(DomainException):
    """
    Exceção lançada quando tentamos criar uma entidade que já existe.
    """
    pass