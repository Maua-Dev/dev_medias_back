from abc import ABC, abstractmethod

from src.shared.domain.entities.user import User


class IUserRepository(ABC):
    @abstractmethod
    def create_user(self, new_user: User) -> User:
        pass

    @abstractmethod
    def get_user(self, user_id: str) -> User:
        pass

    @abstractmethod
    def update_user(self, user: User) -> User:
        pass

    @abstractmethod
    def delete_user(self, user_id: str) -> User:
        pass
