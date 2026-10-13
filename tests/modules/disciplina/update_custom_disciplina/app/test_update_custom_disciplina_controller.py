import pytest

from src.modules.disciplina.update_custom_disciplina.app.update_custom_disciplina_controller import (
    UpdateCustomDisciplinaController,
)
from src.modules.disciplina.update_custom_disciplina.app.update_custom_disciplina_usecase import (
    UpdateCustomDisciplinaUsecase,
)
from src.shared.domain.entities.disciplina import Disciplina, ItemAvaliacao
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.disciplina_repository_mock import DisciplinaRepositoryMock

DEVICE = "550e8400-e29b-41d4-a716-446655440000"
OTHER = "11111111-1111-1111-1111-111111111111"


@pytest.fixture(autouse=True)
def _reset_mock():
    DisciplinaRepositoryMock.reset_store()
    yield
    DisciplinaRepositoryMock.reset_store()


def _seed_custom(device_id: str = DEVICE, code: str = "MIN001") -> None:
    repo = DisciplinaRepositoryMock(user_id=device_id)
    repo.create_disciplina(
        Disciplina(
            course="CUSTOM",
            name="Original",
            code=code,
            period="",
            exam_weight=0.5,
            assignment_weight=0.5,
            exams=[ItemAvaliacao(name="P1", weight=1.0)],
            assignments=[],
            device_id=device_id,
            is_custom=True,
        )
    )


class TestUpdateCustomDisciplinaController:
    def test_success(self):
        _seed_custom()
        repo = DisciplinaRepositoryMock(user_id=DEVICE)
        controller = UpdateCustomDisciplinaController(UpdateCustomDisciplinaUsecase(repo))
        response = controller(
            HttpRequest(
                body={"code": "MIN001", "name": "Atualizado"},
                headers={"X-Device-Id": DEVICE},
            )
        )
        assert response.status_code == 200
        assert response.body["name"] == "Atualizado"

    def test_other_device_gets_404(self):
        _seed_custom(DEVICE)
        repo = DisciplinaRepositoryMock(user_id=OTHER)
        controller = UpdateCustomDisciplinaController(UpdateCustomDisciplinaUsecase(repo))
        response = controller(
            HttpRequest(
                body={"code": "MIN001", "name": "Hack"},
                headers={"X-Device-Id": OTHER},
            )
        )
        assert response.status_code == 404

    def test_catalog_code_not_found_in_device_partition(self):
        repo = DisciplinaRepositoryMock(user_id=DEVICE)
        controller = UpdateCustomDisciplinaController(UpdateCustomDisciplinaUsecase(repo))
        response = controller(
            HttpRequest(
                body={"code": "ECM101", "name": "Hack"},
                headers={"X-Device-Id": DEVICE},
            )
        )
        assert response.status_code == 404
