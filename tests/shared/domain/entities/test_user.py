import pytest
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from pydantic import ValidationError
import uuid

class Test_User:
    
    def test_basic_creation(self):
        id_user = str(uuid.uuid4())
        
        user = User(
        id = id_user,
        name = "João",
        role = ROLE.STUDENT    
        )
        
        assert user.id == id_user
        assert user.name == "João"
        assert user.role == ROLE.STUDENT
    
    def test_id_not_uuid(self):
        with pytest.raises(ValidationError) as err:
            user = User(
            id = 1,
            name = "João",
            role = ROLE.STUDENT    
            )
        
        error = err.value.errors()
        
        assert error[0]["loc"] == ("id",)
        assert error[0]["type"] == "string_type"
        
    
    def test_id_missing(self):
        pass
    
    def test_name_not_str(self):
        pass
    
    def test_role_not_ROLE(self):
        pass
    