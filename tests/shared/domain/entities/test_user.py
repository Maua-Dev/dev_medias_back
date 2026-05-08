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
        user = User(
            name = "João",
            role = ROLE.STUDENT    
            )
        
        assert user.id != None
        assert type(user.id) == str
    
    def test_name_not_str(self):
        with pytest.raises(ValidationError) as err:
            user = User(
            id = str(uuid.uuid4()),
            name = 2,
            role = ROLE.STUDENT    
            )
        
        error = err.value.errors()
        
        assert error[0]["loc"] == ("name",)
        assert error[0]["type"] == "string_type"
        
    def test_name_missing(self):
        with pytest.raises(ValidationError) as err:
            user = User(
            id = str(uuid.uuid4()),
            role = ROLE.STUDENT    
            )
        
        error = err.value.errors()
        
        assert error[0]["loc"] == ("name",)
        assert error[0]["type"] == "missing"
                
    def test_role_not_ROLE(self):
        with pytest.raises(ValidationError) as err:
            user = User(
            id = str(uuid.uuid4()),
            name = "João",
            role = "A"    
            )
        
        error = err.value.errors()
        
        assert error[0]["loc"] == ("role",)
        assert error[0]["type"] == "enum"
    
    def test_role_missing(self):
        user = User(
            id = str(uuid.uuid4()),
            name = "João"
            )
        
        assert user.role != None
        assert type(user.role) == ROLE
        assert user.role == ROLE.STUDENT