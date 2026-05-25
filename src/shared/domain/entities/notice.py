from pydantic import BaseModel, Field
from ..enums.severity_enum import SEVERITY
import uuid

class Notice(BaseModel):
    id:str= Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Id unico do anúncio"
    )
    title: str = Field(
        ...,
        description="Titulo do anúncio",
        max_length=80,
        min_length=1
    )
    description: str = Field (
        description="Descrição do anúncio",
    )
    severity: SEVERITY = Field(
        ...,
        description="Gravidade do anúncio"
    )
    
    
        