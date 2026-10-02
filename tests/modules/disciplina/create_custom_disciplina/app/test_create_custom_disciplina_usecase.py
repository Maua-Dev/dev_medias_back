import pytest

from src.modules.disciplina.create_custom_disciplina.app.create_custom_disciplina_usecase import (
    CreateCustomDisciplinaUsecase,
)
from src.shared.domain.entities.disciplina import Disciplina, ItemAvaliacao
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.infra.repositories.disciplina_repository_mock import DisciplinaRepositoryMock

DEVICE = "550e8400-e29b-41d4-a716-446655440000"


@pytest.fixture(autouse=True)
def _reset_mock():
    DisciplinaRepositoryMock.reset_store()
    yield
    DisciplinaRepositoryMock.reset_store()


def _custom(code: str = "MIN001") -> Disciplina:
    return Disciplina(
        course="CUSTOM",
        name="Custom",
        code=code,
        period="",
        exam_weight=0.5,
        assignment_weight=0.5,
        exams=[ItemAvaliacao(name="P1", weight=1.0)],
        assignments=[],
        courses={},
        device_id=DEVICE,
        is_custom=True,
    )


class TestCreateCustomDisciplinaUsecase:
    def test_success(self):
        repo = DisciplinaRepositoryMock(user_id=DEVICE)
        usecase = CreateCustomDisciplinaUsecase(repo)
        created = usecase(_custom())
        assert created.code == "MIN001"
        assert repo.get_disciplina("MIN001") is not None

    def test_duplicated(self):
        repo = DisciplinaRepositoryMock(user_id=DEVICE)
        usecase = CreateCustomDisciplinaUsecase(repo)
        usecase(_custom())
        with pytest.raises(DuplicatedItem):
            usecase(_custom())
