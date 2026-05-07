from pydantic import *
from ..enums.severity_enum import SEVERITY

class Notice(BaseModel):
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
    
    
        