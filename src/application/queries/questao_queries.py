from dataclasses import dataclass
from uuid import UUID
from typing import Optional

@dataclass
class ObterQuestaoPorIdQuery:
    """
    Query para obter uma questão pelo seu ID.
    Args:
        questao_id (UUID): Identificador único da questão.
    """
    questao_id: UUID

@dataclass
class ObterQuestoesPorUsuarioQuery:
    """
    Query para obter todas as questões de um usuário específico.
    Args:
        usuario (str): Nome do usuário cujas questões serão obtidas.
        limit (Optional[int]): Número máximo de registros a retornar. Padrão: 5.
    """
    usuario: str
    limit: Optional[int] = 5

@dataclass
class ContarQuestoesQuery:
    """
    Query para contar o número de questões, opcionalmente filtradas por usuário.
    Args:
        usuario (Optional[str]): Nome do usuário para filtrar questões.
    """
    usuario: Optional[str] = None
    