import os

import pytest

from src.modules.disciplina.create_custom_disciplina.app.create_custom_disciplina_controller import (
    CreateCustomDisciplinaController,
)
from src.modules.disciplina.create_custom_disciplina.app.create_custom_disciplina_usecase import (
    CreateCustomDisciplinaUsecase,
)
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.disciplina_repository_mock import DisciplinaRepositoryMock

DEVICE = "550e8400-e29b-41d4-a716-446655440000"


@pytest.fixture(autouse=True)
def _reset_mock():
    DisciplinaRepositoryMock.reset_store()
    yield
    DisciplinaRepositoryMock.reset_store()


class TestCreateCustomDisciplinaController:
    def _controller(self):
        repo = DisciplinaRepositoryMock(user_id=DEVICE)
        return CreateCustomDisciplinaController(CreateCustomDisciplinaUsecase(repo))

    def test_success(self):
        request = HttpRequest(
            body={"code": "MIN001", "name": "Minha matéria", "examWeight": 0.7, "assignmentWeight": 0.3},
            headers={"X-Device-Id": DEVICE},
        )
        response = self._controller()(request)
        assert response.status_code == 201
        assert response.body["code"] == "MIN001"
        assert response.body["is_custom"] is True
        assert response.body["device_id"] == DEVICE

    def test_missing_device_id(self):
        request = HttpRequest(body={"code": "MIN001", "name": "X"})
        response = self._controller()(request)
        assert response.status_code == 400

    def test_invalid_device_id(self):
        request = HttpRequest(
            body={"code": "MIN001", "name": "X"},
            headers={"X-Device-Id": "not-a-uuid"},
        )
        response = self._controller()(request)
        assert response.status_code == 400

    def test_missing_code(self):
        request = HttpRequest(body={"name": "X"}, headers={"X-Device-Id": DEVICE})
        response = self._controller()(request)
        assert response.status_code == 400

    def test_conflict(self):
        controller = self._controller()
        body = {"code": "MIN001", "name": "A"}
        headers = {"X-Device-Id": DEVICE}
        assert controller(HttpRequest(body=body, headers=headers)).status_code == 201
        response = controller(HttpRequest(body=body, headers=headers))
        assert response.status_code == 409

    def test_rejects_device_id_in_body(self):
        request = HttpRequest(
            body={"code": "MIN001", "name": "X", "device_id": DEVICE},
            headers={"X-Device-Id": DEVICE},
        )
        response = self._controller()(request)
        assert response.status_code == 400
