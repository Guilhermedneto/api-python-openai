"""
Sanitizador de entrada para prevenir ataques de injeção e XSS.
"""
import re
import html
from typing import Any, Dict, List, Union
import bleach


class InputSanitizer:
    """
    Classe para sanitizar entradas do usuário.
    """
    
    # Padrões perigosos para SQL Injection
    SQL_INJECTION_PATTERNS = [
        r"('|\\'|;|--|/\*|\*/|\bunion\b|\bselect\b|\binsert\b|\bupdate\b|\bdelete\b|\bdrop\b|\bcreate\b|\balter\b|\bexec\b|\bexecute\b|\bscript\b)",
        r"\bOR\b\s*=\s*|\bAND\b\s*=\s*",
        r"\d\s*=\s*\d|\'\s*=\s*\'"
    ]
    
    # Padrões para XSS
    XSS_PATTERNS = [
        r"<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>",
        r"javascript:",
        r"vbscript:",
        r"on\w+\s*=",
        r"<iframe\b",
        r"<object\b",
        r"<embed\b"
    ]
    
    @staticmethod
    def sanitize_string(value: str, max_length: int = 1000) -> str:
        """
        Sanitiza uma string removendo conteúdo perigoso.
        
        Args:
            value: String a ser sanitizada
            max_length: Tamanho máximo permitido
            
        Returns:
            str: String sanitizada
        """
        if not isinstance(value, str):
            return str(value)[:max_length]
        
        # Limita o tamanho
        sanitized = value[:max_length]
        
        # Remove caracteres de controle
        sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', sanitized)
        
        # Escapa HTML para prevenir XSS
        sanitized = html.escape(sanitized)
        
        # Remove padrões suspeitos de SQL injection
        for pattern in InputSanitizer.SQL_INJECTION_PATTERNS:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        # Remove padrões de XSS
        for pattern in InputSanitizer.XSS_PATTERNS:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        return sanitized.strip()
    
    @staticmethod
    def sanitize_email(email: str) -> str:
        """
        Sanitiza e valida um email.
        
        Args:
            email: Email a ser sanitizado
            
        Returns:
            str: Email sanitizado
        """
        if not isinstance(email, str):
            raise ValueError("Email deve ser uma string")
        
        # Remove espaços e converte para minúsculas
        sanitized = email.strip().lower()
        
        # Validação básica de formato
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, sanitized):
            raise ValueError("Formato de email inválido")
        
        # Verifica se contém caracteres perigosos
        dangerous_chars = ['<', '>', '"', "'", '&', '\x00']
        if any(char in sanitized for char in dangerous_chars):
            raise ValueError("Email contém caracteres não permitidos")
        
        return sanitized
    
    @staticmethod
    def sanitize_name(name: str) -> str:
        """
        Sanitiza um nome de pessoa.
        
        Args:
            name: Nome a ser sanitizado
            
        Returns:
            str: Nome sanitizado
        """
        if not isinstance(name, str):
            raise ValueError("Nome deve ser uma string")
        
        # Remove espaços extras e caracteres de controle
        sanitized = re.sub(r'\s+', ' ', name).strip()
        
        # Remove caracteres não alfabéticos (exceto espaços, hífens e apóstrofes)
        sanitized = re.sub(r"[^\w\s\-'áéíóúàèìòùâêîôûãõçÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÃÕÇ]", '', sanitized)
        
        # Verifica tamanho
        if len(sanitized) < 1:
            raise ValueError("Nome não pode estar vazio")
        if len(sanitized) > 200:
            raise ValueError("Nome muito longo (máximo 200 caracteres)")
        
        return sanitized
    
    @staticmethod
    def sanitize_dict(data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitiza recursivamente um dicionário.
        
        Args:
            data: Dicionário a ser sanitizado
            
        Returns:
            Dict: Dicionário sanitizado
        """
        sanitized = {}
        
        for key, value in data.items():
            # Sanitiza a chave
            clean_key = InputSanitizer.sanitize_string(str(key), 100)
            
            # Sanitiza o valor baseado no tipo
            if isinstance(value, str):
                sanitized[clean_key] = InputSanitizer.sanitize_string(value)
            elif isinstance(value, dict):
                sanitized[clean_key] = InputSanitizer.sanitize_dict(value)
            elif isinstance(value, list):
                sanitized[clean_key] = [
                    InputSanitizer.sanitize_string(str(item)) if isinstance(item, str) else item
                    for item in value
                ]
            else:
                sanitized[clean_key] = value
        
        return sanitized
    
    @staticmethod
    def validate_age(age: int) -> int:
        """
        Valida uma idade.
        
        Args:
            age: Idade a ser validada
            
        Returns:
            int: Idade validada
            
        Raises:
            ValueError: Se a idade for inválida
        """
        if not isinstance(age, int):
            raise ValueError("Idade deve ser um número inteiro")
        
        if age < 0:
            raise ValueError("Idade não pode ser negativa")
        
        if age > 150:
            raise ValueError("Idade não pode ser maior que 150 anos")
        
        return age