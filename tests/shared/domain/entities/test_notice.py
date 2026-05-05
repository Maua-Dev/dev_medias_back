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
        
    