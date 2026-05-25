from abc import ABC, abstractmethod
from typing import List
from src.shared.domain.entities.notice import Notice
from src.shared.domain.enums.severity_enum import SEVERITY

class INoticeRepository(ABC):
    @abstractmethod
    def create_notice(self, new_notice: Notice) -> Notice:
        pass
    
    @abstractmethod
    def get_notice(self, notice_id: str) -> Notice:
        pass

    @abstractmethod
    def get_all_notices(self) -> List[Notice]:
        pass
    
    @abstractmethod
    def delete_notice(self, notice_id: str) -> Notice:
        pass
    
    @abstractmethod
    def update_notice(self, 
        id: str,
        title: str,
        description: str,
        severity: SEVERITY
        ) -> Notice:
        pass
    
