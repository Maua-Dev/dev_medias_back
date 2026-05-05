import pytest
from src.shared.domain.entities.notice import Notice
from src.shared.domain.enums.severity_enum import SEVERITY
from pydantic import ValidationError

class TestNotice:
    
    def test_basic_creation(self):
        notice = Notice(title="Titulo", 
                        description="Descrição",
                        severity=SEVERITY.HIGH
                        )
        
        assert notice.title == "Titulo"
        assert notice.description == "Descrição"
        assert notice.severity == SEVERITY.HIGH
    
    # Title specific errors:
    def test_title_have_more_than_80_characters(self):
        with pytest.raises(ValidationError) as err:
            notice = Notice(title="Tituloooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo", 
            description="Descrição",
            severity=SEVERITY.HIGH
            )
            
        error = err.value.errors()
        
        assert error[0]["loc"] == ("title",)
        assert error[0]["type"] == "string_too_long" 
            
    def test_title_is_missing(self):
        with pytest.raises(ValidationError) as err:
            notice = Notice(              
            description="Descrição",
            severity=SEVERITY.HIGH
            )
        error = err.value.errors()
        
        assert error[0]["loc"] == ("title",)
        assert error[0]["type"] == "missing"
    
    def test_title_type_mismatch(self):
        with pytest.raises(ValidationError) as err:
            notice = Notice(
            title=1,
            description="Descrição",
            severity=SEVERITY.HIGH
            )
        error = err.value.errors()
        
        assert error[0]["loc"] == ("title",)
        assert error[0]["type"] == "string_type"
        
    #Description specific errors:
    def test_description_is_missing(self):
        with pytest.raises(ValidationError) as err:
            notice = Notice(
                title="Titulo", 
                severity=SEVERITY.HIGH
                )
        error = err.value.errors()
        
        assert error[0]["loc"] == ("description",)
        assert error[0]["type"] == "missing"
        
    def test_description_type_mismatch(self):
        with pytest.raises(ValidationError) as err:
            notice = Notice(
                title="Titulo",
                description=1,
                severity=SEVERITY.HIGH
            )
        error = err.value.errors()
        
        assert error[0]["loc"] == ("description",)
        assert error[0]["type"] == "string_type"
    
    #Severity specific errors:      
    def test_severity_is_missing(self):
        with pytest.raises(ValidationError) as err:
            notice = Notice(
                title="Titulo",
                description="Descrição"
            )
        error = err.value.errors()
        
        assert error[0]["loc"] == ("severity",)
        assert error[0]["type"] == "missing"   
        
    def test_severity_type_mismatch(self):
        with pytest.raises(ValidationError) as err:
            notice = Notice(
                title="Titulo",
                description="Descrição",
                severity=1
            )
        error = err.value.errors()
        
        assert error[0]["loc"] == ("severity",)
        assert error[0]["type"] == 'enum'