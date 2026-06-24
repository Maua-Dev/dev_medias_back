from ...domain.repositories.notice.notice_repository_interface import INoticeRepository
from ...domain.entities.notice import Notice
from typing import List
from uuid import uuid4
from ...domain.enums.severity_enum import SEVERITY
from ...helpers.errors.controller_errors import MissingParameters

class NoticeRepositoryMock(INoticeRepository):
    notice: List[Notice]
    
    def __init__(self):
        self.notice = [
            Notice(
                id=str(uuid4()),
                title="Aviso 1",
                description="Muito importante",
                severity=SEVERITY.HIGH
            ),
            Notice(
                id=str(uuid4()),
                title="Aviso 2",
                description="Mais ou menos importante",
                severity=SEVERITY.MEDIUM
            ),
            Notice(
                id=str(uuid4()),
                title="Aviso 3",
                description="Pouco importante",
                severity=SEVERITY.LOW
            )
        ]

    def get_notice(self, notice_id) -> Notice:
        for notice in self.notice:
            if notice.id == notice_id:
                return notice       
        return None
    
    def get_all_notices(self) -> List[Notice]:
        return self.notice
    
    def create_notice(self, new_notice):
        self.notice.append(new_notice)
        return new_notice
    
    def update_notice(self, 
                      id:str,
                      title:str,
                      description:str,
                      severity: SEVERITY):
        
        notice = self.get_notice(notice_id=id)
        if id == None:
            raise MissingParameters(message="id")
        if notice == None:
            raise ValueError("Notice not found")
        
        if title is not None:
            notice.title = title
        
        if description is not None:
            notice.description = description
    
        if severity is not None:
            notice.severity = severity
        
        return notice
        
    
    def delete_notice(self, notice_id):
        notice = self.get_notice(notice_id=notice_id)
        if notice is None:
            raise ValueError("Notice not found")

        self.notice.remove(notice)
        return notice
    
