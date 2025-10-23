from dataclasses import dataclass
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Questao:
    """
    Representa uma questão com pergunta e resposta.
    Attributes:
        id (UUID): Identificador único da questão.
        texto_pergunta (str): Texto da pergunta.
        texto_resposta (str): Texto da resposta.
        data_criacao (datetime): Data e hora de criação da questão.
    """
    id: UUID
    texto_pergunta: str
    texto_resposta: str
    usuario: str
    data_criacao: datetime

    def __init__(self, id: UUID, 
              texto_pergunta: str, 
              texto_resposta: str, 
              usuario: str,
              data_criacao: datetime = None):
        """
        Inicializa uma nova instância de Questao.
        Args:
            id (UUID): Identificador único da questão.
            texto_pergunta (str): Texto da pergunta.
            texto_resposta (str): Texto da resposta.
            data_criacao (datetime, optional): Data e hora de criação da questão. 
                                            Se não fornecido, usa a data atual.
        """
        if not texto_pergunta or not texto_pergunta.strip():
            raise ValueError("A pergunta não pode ser vazia.")
        
        if not texto_resposta or not texto_resposta.strip():
            raise ValueError("A resposta não pode ser vazia.")

        if len(texto_pergunta.strip()) < 1:
            raise ValueError("A pergunta deve ter pelo menos 1 caracter.")
        
        self.id = id or uuid4()
        self.texto_pergunta = texto_pergunta.strip()
        self.texto_resposta = texto_resposta.strip()
        self.usuario = usuario.strip()
        self.data_criacao = data_criacao or datetime.utcnow()
        
        def __str__(self) -> str:
            return f"Questao(id={self.id}, pergunta={self.texto_pergunta}, resposta={self.texto_resposta}, usuario={self.usuario}, data_criacao={self.data_criacao})"

        def __repr__(self) -> str:
            return self.__str__()
        