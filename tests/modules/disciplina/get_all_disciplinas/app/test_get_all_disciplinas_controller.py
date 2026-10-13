import os

import pytest

from src.modules.disciplina.get_all_disciplinas.app.get_all_disciplinas_controller import (
    GetAllDisciplinasController,
)
from src.modules.disciplina.get_all_disciplinas.app.get_all_disciplinas_usecase import (
    GetAllDisciplinasUsecase,
)
from src.shared.domain.entities.disciplina import Disciplina, ItemAvaliacao
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.disciplina_repository_mock import DisciplinaRepositoryMock

DEVICE = "550e8400-e29b-41d4-a716-446655440000"


@pytest.fixture(autouse=True)
def _reset_mock(monkeypatch):
    monkeypatch.setenv("STAGE", "TEST")
    DisciplinaRepositoryMock.reset_store()
    yield
    DisciplinaRepositoryMock.reset_store()


class TestGetAllDisciplinasController:
    def test_get_all_disciplinas_controller_success(self):
        request = HttpRequest()
        usecase = GetAllDisciplinasUsecase(repository=DisciplinaRepositoryMock())
        controller = GetAllDisciplinasController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 200
        assert isinstance(response.body, list)
        assert response.body[0]["code"] == "ECM101"
        assert response.body[0]["is_custom"] is False

    def test_merges_custom_when_device_id_present(self):
        device_repo = DisciplinaRepositoryMock(user_id=DEVICE)
        device_repo.create_disciplina(
            Disciplina(
                course="CUSTOM",
                name="Minha",
                code="MIN001",
                period="",
                exam_weight=0.5,
                assignment_weight=0.5,
                exams=[ItemAvaliacao(name="P1", weight=1.0)],
                assignments=[],
                device_id=DEVICE,
                is_custom=True,
            )
        )
        request = HttpRequest(headers={"X-Device-Id": DEVICE})
        usecase = GetAllDisciplinasUsecase(repository=DisciplinaRepositoryMock())
        controller = GetAllDisciplinasController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 200
        codes = [item["code"] for item in response.body]
        assert "ECM101" in codes
        assert "MIN001" in codes
        custom = next(item for item in response.body if item["code"] == "MIN001")
        assert custom["is_custom"] is True

    def test_invalid_device_id_returns_400(self):
        request = HttpRequest(headers={"X-Device-Id": "bad"})
        usecase = GetAllDisciplinasUsecase(repository=DisciplinaRepositoryMock())
        controller = GetAllDisciplinasController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400

    def test_get_all_disciplinas_controller_not_found(self):
        request = HttpRequest()
        repository = DisciplinaRepositoryMock()
        repository.disciplinas = []
        usecase = GetAllDisciplinasUsecase(repository=repository)
        controller = GetAllDisciplinasController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 404
        assert "No items found for disciplinas" in str(response.body)

    def test_get_all_disciplinas_controller_internal_server_error(self):
        from unittest.mock import MagicMock

        request = HttpRequest()
        usecase = MagicMock(side_effect=Exception("unexpected failure"))
        controller = GetAllDisciplinasController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 500
        assert str(response.body) == "unexpected failure"
