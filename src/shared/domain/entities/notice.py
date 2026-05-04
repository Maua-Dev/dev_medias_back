from src.shared.helpers.errors.domain_errors import EntityError, EntityParameterError
from pydantic import *
from ..enums.severity_enum import severity

class notice(BaseModel):
    title: str = Field(
        description="Titulo do anúncio",
        min_length=1,
        max_length=10
    )
    description: str = Field (
        description="Descrição do anúncio",
    )
    severity: severity = Field(
        description="Gravidade do anúncio"
    )
    
    
        