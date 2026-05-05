import pytest
from src.shared.domain.entities.notice import Notice
from src.shared.domain.enums.severity_enum import SEVERITY
from pydantic import ValidationError

class Test_Notice:
    
    def test_basic_creation(self):
        notice = Notice(title="Titulo", 
                        description="Descrição",
                        severity=SEVERITY.HIGH
                        )
        
        assert notice.title == "Titulo"
        assert notice.description == "Descrição"
        assert notice.severity == SEVERITY.HIGH
        
    def test_title_have_more_than_80_characters(self):
        with pytest.raises(ValidationError) as err:
            notice = Notice(title="Tituloooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo", 
            description="Descrição",
            severity=SEVERITY.HIGH
            )
            
            error = err.value.errors()
            
            assert error[0]["loc"] == "title"
            assert error[0]["type"] == "string_too_long" 