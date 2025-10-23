from dataclasses import dataclass
from typing import Optional

@dataclass
class CriarQuestaoCommand:
    """
    Comando para criar uma nova questão.
    
    Args:
        texto_pergunta (str): Texto da pergunta enviada pelo usuário.
        texto_resposta (Optional[str]): Texto da resposta gerada pela OpenAI (preenchido pelo sistema).
        usuario (str): Usuário que criou a questão.
    """
    texto_pergunta: str
    usuario: str
    texto_resposta: Optional[str] = None
    
    
    