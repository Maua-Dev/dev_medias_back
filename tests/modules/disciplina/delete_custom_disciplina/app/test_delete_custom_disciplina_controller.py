import pytest

from src.modules.disciplina.delete_custom_disciplina.app.delete_custom_disciplina_controller import (
    DeleteCustomDisciplinaController,
)
from src.modules.disciplina.delete_custom_disciplina.app.delete_custom_disciplina_usecase import (
    DeleteCustomDisciplinaUsecase,
)
from src.shared.domain.entities.disciplina import Disciplina, ItemAvaliacao
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.disciplina_repository_mock import DisciplinaRepositoryMock

DEVICE = "550e8400-e29b-41d4-a716-446655440000"


@pytest.fixture(autouse=True)
def _reset_mock():
    DisciplinaRepositoryMock.reset_store()
    yield
    DisciplinaRepositoryMock.reset_store()


class TestDeleteCustomDisciplinaController:
    def test_success(self):
        repo = DisciplinaRepositoryMock(user_id=DEVICE)
        repo.create_disciplina(
            Disciplina(
                course="CUSTOM",
                name="X",
                code="MIN001",
                period="",
                exam_weight=0.5,
                assignment_weight=0.5,
                exams=[],
                assignments=[],
                device_id=DEVICE,
                is_custom=True,
            )
        )
        controller = DeleteCustomDisciplinaController(DeleteCustomDisciplinaUsecase(repo))
        response = controller(
            HttpRequest(
                body={"code": "MIN001"},
                headers={"X-Device-Id": DEVICE},
            )
        )
        assert response.status_code == 200
        assert response.body["code"] == "MIN001"
        assert repo.get_disciplina("MIN001") is None

    def test_catalog_not_deletable_via_device_repo(self):
        repo = DisciplinaRepositoryMock(user_id=DEVICE)
        controller = DeleteCustomDisciplinaController(DeleteCustomDisciplinaUsecase(repo))
        response = controller(
            HttpRequest(
                query_params={"code": "ECM101"},
                headers={"X-Device-Id": DEVICE},
            )
        )
        assert response.status_code == 404
        # GLOBAL catalog untouched
        assert DisciplinaRepositoryMock().get_disciplina("ECM101") is not None
