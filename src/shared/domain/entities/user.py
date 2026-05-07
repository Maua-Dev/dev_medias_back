from pydantic import *
from ..enums.role_enum import ROLE
import uuid

class User(BaseModel):
    id:str= Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Id unico do usuário"
    )
    
    name:str = Field(
        ...,
        description="Nome do usuario"
    )
    
    role:ROLE = Field(
        default=ROLE.STUDENT,
        description="Role do usuario"
    )
