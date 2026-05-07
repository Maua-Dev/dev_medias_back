from pydantic import *
from ..enums.role_enum import ROLE
import uuid

class user:
    id:str= Field(
        description="Id unico do usuário",
        default_factory=lambda: str(uuid.uuid4())
    )
    
    name:str = Field(
        description="Nome do usuario"
    )
    
    role:ROLE = Field(
        description="Role do usuario"
    )
