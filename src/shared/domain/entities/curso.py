from pydantic import BaseModel, Field


class Curso(BaseModel):
    
    código: str = Field(..., description="Identificador do curso")
    nome: str = Field(..., description="Nome do curso")

