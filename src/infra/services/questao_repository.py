


from sqlite3 import IntegrityError
from src.domain.entities.questao import Questao
from src.domain.repositories.iquestao_repository import IQuestaoRepository
from src.infra.mappers.questao_mapper import QuestaoMapper
from src.infra.applicationBdContext.database import get_database_config


class QuestaoRepository(IQuestaoRepository):
    async def contar_questoes(self, query) -> int:
        session = None
        try:
            session = self._get_session()
            stmt = session.query(QuestaoMapper.model_class())
            if hasattr(query, 'usuario_id') and query.usuario_id:
                stmt = stmt.filter(QuestaoMapper.model_class().usuario_id == query.usuario_id)
            count = await stmt.count()
            return count
        finally:
            if session:
                session.close()
    def __init__(self):
        # Inicialização do repositório, como conexão com o banco de dados
       self.db_config = get_database_config()
       
    def _get_session(self):
        # Método privado para obter uma sessão de banco de dados
        return self.db_config.get_session()

    async def criar_questao(self, questao: Questao) -> Questao:
        session = None
        try:
            session = self._get_session()
            model = QuestaoMapper.to_model(questao)
            session.add(model)
            session.commit()
            session.refresh(model)
            return QuestaoMapper.to_entity(model)
        except IntegrityError as e:
            session.rollback()
            raise Exception(f"Erro de integridade ao criar questão: {e}")
        finally:
            if session:
                session.close()
                
    
    async def obter_questao_por_id(self, query) -> Questao:
        session = None
        try:
            session = self._get_session()
            model = session.get(QuestaoMapper.model_class(), query.questao_id)
            if model:
                return QuestaoMapper.to_entity(model)
            return None
        finally:
            if session:
                session.close()

    async def listar_questoes_por_usuario(self, query, limit: int = 5) -> list[Questao]:
        session = None
        try:
            session = self._get_session()
            stmt = session.query(QuestaoMapper.model_class())
            # Filtrar pelo campo 'usuario' (ajuste conforme o nome do campo na model)
            if query.usuario:
                stmt = stmt.filter(QuestaoMapper.model_class().usuario == query.usuario)
            # Ordenar por data de criação decrescente
            stmt = stmt.order_by(QuestaoMapper.model_class().data_criacao.desc())
            # Aplicar limitação
            stmt = stmt.limit(limit)
            results = stmt.all()
            return [QuestaoMapper.to_entity(model) for model in results]
        finally:
            if session:
                session.close()
    
    
