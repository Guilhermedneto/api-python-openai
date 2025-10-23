

from src.domain.entities.questao import Questao
from src.infra.applicationBdContext.database import QuestaoModel


class QuestaoMapper:
    @staticmethod
    def model_class():
        """Retorna a classe do modelo QuestaoModel."""
        from src.infra.applicationBdContext.database import QuestaoModel
        return QuestaoModel
    @staticmethod
    def to_model(questao: Questao) -> QuestaoModel:
        """Mapeia uma entidade Questao para um modelo QuestaoModel.
        
        Args:
            questao (Questao): A entidade Questao a ser mapeada.
        
        Returns:
            QuestaoModel: O modelo QuestaoModel correspondente.
        """
        return QuestaoModel(
            id=questao.id,
            texto_pergunta=questao.texto_pergunta,
            texto_resposta=questao.texto_resposta,
            usuario=questao.usuario,
            data_criacao=questao.data_criacao
        )

    @staticmethod
    def to_entity(model: QuestaoModel) -> Questao:
        """Mapeia um modelo QuestaoModel para uma entidade Questao.
        
        Args:
            model (QuestaoModel): O modelo QuestaoModel a ser mapeado.
        
        Returns:
            Questao: A entidade Questao correspondente.
        """
        return Questao(
            id=model.id,
            texto_pergunta=model.texto_pergunta,
            texto_resposta=model.texto_resposta,
            usuario=model.usuario,
            data_criacao=model.data_criacao
        )
    

