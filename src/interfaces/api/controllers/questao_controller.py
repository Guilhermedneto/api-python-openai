

from fastapi import APIRouter, HTTPException, status, Depends
from uuid import UUID
from src.interfaces.api.models.questao_models import CriarQuestaoCommand, ListarQuestoesResponseModel, QuestaoResponseModel, ErrorResponseModel
from src.application.queries.questao_queries import ObterQuestaoPorIdQuery, ObterQuestoesPorUsuarioQuery

def get_questao_service():
    from src.application.services.questao_service import QuestaoService
    from src.infra.services.questao_repository import QuestaoRepository
    from src.application.services.openai_service import OpenAIService
    return QuestaoService(QuestaoRepository(), OpenAIService())

router = APIRouter(prefix="/questoes", tags=["Questões"])

@router.post(
    "/",
    response_model=QuestaoResponseModel,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma nova questão",
    description="Recebe uma pergunta, consulta a OpenAI, salva e retorna o registro.",
    responses={201: {"model": QuestaoResponseModel, "description": "Questão criada com sucesso"},
               500: {"description": "Erro interno do servidor"}}
)
async def criar_questao(
    command: CriarQuestaoCommand,
    questao_service=Depends(get_questao_service)
):
    from src.interfaces.shared.security.input_sanitizer import InputSanitizer
    command.texto_pergunta = InputSanitizer.sanitize_string(command.texto_pergunta, 1000)
    if hasattr(command, "texto_resposta") and command.texto_resposta:
        command.texto_resposta = InputSanitizer.sanitize_string(command.texto_resposta, 4000)
    if hasattr(command, "usuario") and command.usuario:
        command.usuario = InputSanitizer.sanitize_name(command.usuario)
    questao = await questao_service.criar_questao(command)
    return QuestaoResponseModel.from_orm(questao)

@router.get(
    "/{questao_id}",
    response_model=QuestaoResponseModel,
    status_code=status.HTTP_200_OK,
    summary="Obtém uma questão pelo ID",
    description="Obtém uma questão específica pelo seu ID.",
    responses={200: {"model": QuestaoResponseModel, "description": "Questão obtida com sucesso"},
               404: {"model": ErrorResponseModel, "description": "Questão não encontrada"},
               500: {"model": ErrorResponseModel, "description": "Erro interno do servidor"}}
)
async def obter_questao_por_id(
    questao_id: UUID,
    questao_service=Depends(get_questao_service)
):
    query = ObterQuestaoPorIdQuery(questao_id=questao_id)
    questao = await questao_service.obter_questao_por_id(query)
    if questao is None:
        raise HTTPException(status_code=404, detail="Questão não encontrada")
    return QuestaoResponseModel.from_orm(questao)

@router.get(
    "/usuario/{usuario}",
    response_model=ListarQuestoesResponseModel
)
async def listar_questoes_por_usuario(
    usuario: str,
    questao_service=Depends(get_questao_service)
):
    query = ObterQuestoesPorUsuarioQuery(usuario=usuario)
    questoes = await questao_service.listar_questoes_por_usuario(query)
    return ListarQuestoesResponseModel(
        questoes=[QuestaoResponseModel.from_orm(q) for q in questoes]
    )