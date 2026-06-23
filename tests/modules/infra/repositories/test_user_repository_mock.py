import pytest
import uuid

from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import ROLE
from src.shared.infra.repositories.user_repository_mock import UserRepositoryMock


class Test_UserRepositoryMock:
    def test_create_user(self):
        repo = UserRepositoryMock()
        user = User(id=str(uuid.uuid4()), name="Guilherme", role=ROLE.STUDENT)

        created = repo.create_user(user)

        assert created is user
        assert repo.get_user(user.id) == user

    def test_get_user_returns_stored_user(self):
        repo = UserRepositoryMock()
        user = User(id=str(uuid.uuid4()), name="Guilherme", role=ROLE.STUDENT)
        repo.create_user(user)

        fetched = repo.get_user(user.id)

        assert fetched == user

    def test_get_user_not_found_raises(self):
        repo = UserRepositoryMock()

        with pytest.raises(ValueError, match="not found"):
            repo.get_user("missing-id")

    def test_update_user_replaces_user_in_store(self):
        repo = UserRepositoryMock()
        user = User(id=str(uuid.uuid4()), name="Guilherme", role=ROLE.STUDENT)
        repo.create_user(user)

        updated = User(id=user.id, name="Guilherme 43", role=ROLE.ADMIN)
        result = repo.update_user(updated)

        assert result == updated
        assert repo.get_user(user.id).name == "Guilherme 43"
        assert repo.get_user(user.id).role == ROLE.ADMIN

    def test_update_user_not_found_raises(self):
        repo = UserRepositoryMock()
        new_user = User(id=str(uuid.uuid4()), name="Guilherme", role=ROLE.STUDENT)

        with pytest.raises(ValueError, match="not found"):
            repo.update_user(new_user)

    def test_delete_user_returns_deleted_user(self):
        repo = UserRepositoryMock()
        user = User(id=str(uuid.uuid4()), name="Guilherme", role=ROLE.STUDENT)
        repo.create_user(user)

        deleted = repo.delete_user(user.id)

        assert deleted == user
        with pytest.raises(ValueError, match="not found"):
            repo.get_user(user.id)

    def test_delete_user_not_found_raises(self):
        repo = UserRepositoryMock()

        with pytest.raises(ValueError, match="not found"):
            repo.delete_user("missing-id")
