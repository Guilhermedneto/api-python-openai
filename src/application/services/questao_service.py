from .openai_service import OpenAIService
from typing import List, Optional
from uuid import UUID
from ...domain.entities.questao import Questao
from ...domain.repositories.iquestao_repository import IQuestaoRepository
from ..commands.questao_commands import CriarQuestaoCommand
from ..queries.questao_queries import ContarQuestoesQuery, ObterQuestaoPorIdQuery, ObterQuestoesPorUsuarioQuery
from ..interfaces.iquestao_service import IQuestaoService
from datetime import datetime


class QuestaoService(IQuestaoService):
    def __init__(self, questao_repository: IQuestaoRepository, openai_service: OpenAIService):
        self._questao_repository = questao_repository
        self._openai_service = openai_service

    async def criar_questao(self, command: CriarQuestaoCommand) -> Questao:
        # 1. Buscar histórico das últimas 5 perguntas e respostas do usuário
        from src.application.queries.questao_queries import ObterQuestoesPorUsuarioQuery
        historico_query = ObterQuestoesPorUsuarioQuery(usuario=command.usuario)
        historico = await self._questao_repository.listar_questoes_por_usuario(historico_query, limit=5)

        # 2. Montar o contexto de mensagens para o chat
        chat_prompt = [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "Você é um assistente de IA que ajuda as pessoas a encontrar informações."
                    }
                ]
            }
        ]
        # Adiciona histórico ao prompt
        for q in reversed(historico):  # do mais antigo para o mais recente
            chat_prompt.append({
                "role": "user",
                "content": [
                    {"type": "text", "text": q.texto_pergunta}
                ]
            })
            chat_prompt.append({
                "role": "assistant",
                "content": [
                    {"type": "text", "text": q.texto_resposta}
                ]
            })
        # Adiciona a nova pergunta
        chat_prompt.append({
            "role": "user",
            "content": [
                {"type": "text", "text": command.texto_pergunta}
            ]
        })

        # 3. Chama OpenAIService passando o contexto
        texto_resposta = self._openai_service.perguntar_com_contexto(chat_prompt)

        # 4. Persiste a nova pergunta e resposta
        nova_questao = Questao(
            id=None,
            texto_pergunta=command.texto_pergunta,
            texto_resposta=texto_resposta,
            usuario=command.usuario,
            data_criacao=datetime.utcnow()
        )
        # Tenta serializar antes de salvar
        from src.interfaces.api.models.questao_models import QuestaoResponseModel
        try:
            _ = QuestaoResponseModel.from_orm(nova_questao)
        except Exception as e:
            raise Exception(f"Erro ao serializar resposta: {e}")
        questao_salva = await self._questao_repository.criar_questao(nova_questao)
        return questao_salva

    async def obter_questao_por_id(self, query: ObterQuestaoPorIdQuery) -> Optional[Questao]:
        return await self._questao_repository.obter_questao_por_id(query)

    async def listar_questoes_por_usuario(self, query: ObterQuestoesPorUsuarioQuery) -> List[Questao]:
        return await self._questao_repository.listar_questoes_por_usuario(query)

    async def contar_questoes(self, query: ContarQuestoesQuery) -> int:
        return await self._questao_repository.contar_questoes(query)

