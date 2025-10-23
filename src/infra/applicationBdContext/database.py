from sqlalchemy import Column, String, DateTime, create_engine, text
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import TypeDecorator, CHAR
from uuid import uuid4
import uuid

Base = declarative_base()

class GUID(TypeDecorator):
    """
    Tipo UUID para SQL Server.
    """
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        return dialect.type_descriptor(UNIQUEIDENTIFIER())

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        return str(value)

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                return uuid.UUID(value)
            return value

class QuestaoModel(Base):
    """
    Modelo SQLAlchemy para a tabela de questões.
    """
    __tablename__ = "questoes"
    id = Column(GUID(), primary_key=True, default=uuid4, nullable=False)
    texto_pergunta = Column(String(1000), nullable=False)
    texto_resposta = Column(String(4000), nullable=False)
    usuario = Column(String(255), nullable=False)
    data_criacao = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<QuestaoModel(id={self.id}, texto_pergunta='{self.texto_pergunta}', texto_resposta='{self.texto_resposta}', usuario='{self.usuario}', data_criacao='{self.data_criacao}')>"

class DatabaseConfig:
    """
    Configuração do banco de dados SQL Server.
    """
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_engine(
            database_url,
            echo=True,  # Mude para True para ver as queries SQL
            pool_pre_ping=True,
            pool_recycle=3600,
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def create_database_if_not_exists(self, database_name: str = "UsuariosDB"):
        try:
            master_url = self.database_url.replace(f"/{database_name}", "/master")
            master_engine = create_engine(master_url)
            with master_engine.connect() as conn:
                result = conn.execute(
                    text("SELECT database_id FROM sys.databases WHERE name = :db_name"),
                    {"db_name": database_name}
                )
                if result.fetchone() is None:
                    conn.execute(text(f"CREATE DATABASE [{database_name}]"))
                    conn.commit()
                    print(f"✅ Banco de dados '{database_name}' criado com sucesso!")
                else:
                    print(f"ℹ️ Banco de dados '{database_name}' já existe.")
        except Exception as e:
            print(f"⚠️ Erro ao criar banco de dados: {e}")

    def create_tables(self):
        self.create_database_if_not_exists()
        Base.metadata.create_all(bind=self.engine)
        print("✅ Tabelas criadas/verificadas com sucesso!")

    def get_session(self):
        return self.SessionLocal()

    def get_db_session(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

db_config: DatabaseConfig = None

def initialize_database(database_url: str):
    global db_config
    db_config = DatabaseConfig(database_url)
    db_config.create_tables()

def get_database_config() -> DatabaseConfig:
    if db_config is None:
        raise RuntimeError("Banco de dados não foi inicializado. Chame initialize_database() primeiro.")
    return db_config