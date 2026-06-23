from typing import Dict

from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user.user_repository_interface import IUserRepository


class UserRepositoryMock(IUserRepository):
    def __init__(self) -> None:
        self._users: Dict[str, User] = {}

    def create_user(self, new_user: User) -> User:
        self._users[new_user.id] = new_user
        return new_user

    def get_user(self, user_id: str) -> User:
        user = self._users.get(user_id)
        if user is None:
            raise ValueError(f"User with id '{user_id}' not found")
        return user

    def update_user(self, user: User) -> User:
        if user.id not in self._users:
            raise ValueError(f"User with id '{user.id}' not found")
        self._users[user.id] = user
        return user

    def delete_user(self, user_id: str) -> User:
        if user_id not in self._users:
            raise ValueError(f"User with id '{user_id}' not found")
        return self._users.pop(user_id)
