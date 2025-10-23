from src.application.commands.questao_commands import CriarQuestaoCommand
from src.application.commands.create_questao_command_validation import CreateQuestaoCommandValidation
from src.domain.entities.questao import Questao
from src.infra.mappers.questao_mapper import QuestaoMapper
from src.infra.applicationBdContext.database import get_database_config

class CreateQuestaoCommandHandler:
    def __init__(self, questao_service):
        self.validator = CreateQuestaoCommandValidation()
        self._questao_service = questao_service

    async def handle(self, command: CriarQuestaoCommand):
        # Validação
        self.validator.validate(command)
        # Delegação para o service, que cuida da criação, geração de id/data e persistência
        questao = await self._questao_service.criar_questao(command)
        return questao
