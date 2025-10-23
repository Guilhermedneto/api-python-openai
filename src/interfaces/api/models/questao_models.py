from typing import List
from pydantic import BaseModel, Field
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from typing import Optional
from datetime import datetime



class CriarQuestaoCommand(BaseModel):
    usuario: str = Field(..., description="Usuário que criou a questão")
    texto_pergunta: str = Field(..., description="Texto da pergunta")

    class Config:
        json_schema_extra = {
            "example": {
                "usuario": "usuario_exemplo",
                "texto_pergunta": "Qual é a capital da França?"
            }
        }


class QuestaoResponseModel(BaseModel):
    id: UUID = Field(..., description="Identificador único da questão")
    usuario: str = Field(..., description="Usuário que criou a questão")
    texto_pergunta: str = Field(..., description="Texto da pergunta")
    texto_resposta: str = Field(..., description="Texto da resposta")
    data_criacao: datetime = Field(..., description="Data e hora de criação da questão")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "usuario": "usuario_exemplo",
                "texto_pergunta": "Qual é a capital da França?",
                "texto_resposta": "Paris",
                "data_criacao": "2024-01-01T12:00:00Z"
            }
        }

class ListarQuestoesResponseModel(BaseModel):
    questoes: List[QuestaoResponseModel] = Field(..., description="Lista de questões")
    
    class Config:
        json_schema_extra = {
            "example": {
                "questoes": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "usuario": "usuario_exemplo",
                        "texto_pergunta": "Qual é a capital da França?",
                        "texto_resposta": "Paris",
                        "data_criacao": "2024-01-01T12:00:00Z"
                    },
                    {
                        "id": "223e4567-e89b-12d3-a456-426614174001",
                        "usuario": "usuario_exemplo2",
                        "texto_pergunta": "Qual é a capital da Alemanha?",
                        "texto_resposta": "Berlim",
                        "data_criacao": "2024-01-02T12:00:00Z"
                    }
                ]
            }
        }

class ListarQuestoesQueryModel(BaseModel):
    usuario: str = Field(None, description="Nome do usuário para filtrar questões")
    
    class Config:
        json_schema_extra = {
            "example": {
                "usuario": "usuario_exemplo"
            }
        }


class ErrorResponseModel(BaseModel):
    detail: str = Field(..., description="Detalhes do erro")
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Questão não encontrada."
            }
        }

