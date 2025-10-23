from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from uuid import UUID
from ...domain.entities.questao import Questao
from ..commands.questao_commands import CriarQuestaoCommand
from ..queries.questao_queries import ContarQuestoesQuery, ObterQuestaoPorIdQuery, ObterQuestoesPorUsuarioQuery


class IQuestaoService(ABC):
    @abstractmethod
    async def criar_questao(self, command: CriarQuestaoCommand) -> Questao:
        """Cria uma nova questão.
        Args:
            command (CriarQuestaoCommand): Comando contendo os dados da questão a ser criada
        Returns:
            Questao: A questão criada.
            
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
        """Lista questões, opcionalmente filtradas por usuário.
        Args:
            query (Optional[str]): Nome do usuário para filtrar questões.
        Returns:
            List[Questao]: Lista de questões.
        """
        pass

    @abstractmethod
    async def contar_questoes(self, query: ContarQuestoesQuery) -> int:
        """Conta o número de questões, opcionalmente filtradas por usuário.
        Args:
            query (ContarQuestoesQuery): Query contendo os critérios de filtragem.
        Returns:
            int: O número de questões que atendem aos critérios.
        """
        pass