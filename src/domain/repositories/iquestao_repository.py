

from abc import ABC, abstractmethod
from typing import List, Optional

from src.application.commands.questao_commands import CriarQuestaoCommand
from src.application.queries.questao_queries import ContarQuestoesQuery, ObterQuestaoPorIdQuery, ObterQuestoesPorUsuarioQuery
from src.domain.entities.questao import Questao


class IQuestaoRepository(ABC):
    
    """
    Interface do repositório de questões.
    Define os contratos para persistência e recuperação de questões.
    """
    
    
    @abstractmethod
    async def criar_questao(self, questao: Questao) -> Questao:
        """Cria uma nova questão no repositório.
        
        Args:
            questao (Questao): A questão a ser criada.
        
        Returns:
            Questao: A questão criada com ID atribuído.
        """
        pass
    
    @abstractmethod
    async def obter_questao_por_id(self, query: ObterQuestaoPorIdQuery) -> Optional[Questao]:
        """Obtém uma questão pelo seu ID.
        
        Args:
            query (ObterQuestaoQuery): Query contendo o ID da questão a ser obtida.
        
        Returns:
            Optional[Questao]: A questão obtida ou None se não encontrada.
        """
        pass

    @abstractmethod
    async def listar_questoes_por_usuario(self, query: ObterQuestoesPorUsuarioQuery) -> List[Questao]:
        """
        Lista as questões de um usuário, limitando o número de registros conforme especificado.
        Args:
            query (ObterQuestoesPorUsuarioQuery): Query contendo o usuário e o limite de registros.
        Returns:
            List[Questao]: Lista de questões do usuário, limitada pelo parâmetro 'limit'.
        """
        pass

    @abstractmethod
    async def contar_questoes(self, query: ContarQuestoesQuery) -> int:
        """Conta o número de questões no repositório, opcionalmente filtradas por usuário.
        Args:
            query (ContarQuestoesQuery): Query contendo os critérios de filtragem.
        Returns:
            int: O número de questões que atendem aos critérios.
        """
        pass