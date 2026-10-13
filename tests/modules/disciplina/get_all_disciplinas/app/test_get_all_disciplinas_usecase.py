import pytest

from src.modules.disciplina.get_all_disciplinas.app.get_all_disciplinas_usecase import GetAllDisciplinasUsecase
from src.shared.domain.entities.disciplina import Disciplina, ItemAvaliacao
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.disciplina_repository_mock import DisciplinaRepositoryMock

DEVICE = "550e8400-e29b-41d4-a716-446655440000"


@pytest.fixture(autouse=True)
def _reset_mock(monkeypatch):
    monkeypatch.setenv("STAGE", "TEST")
    DisciplinaRepositoryMock.reset_store()
    yield
    DisciplinaRepositoryMock.reset_store()


class TestGetAllDisciplinasUsecase:
    def test_get_all_disciplinas_usecase_success(self):
        repository = DisciplinaRepositoryMock()
        usecase = GetAllDisciplinasUsecase(repository)

        response = usecase()

        assert len(response) == 4
        assert response[0].code == "ECM101"

    def test_merges_device_customs(self):
        DisciplinaRepositoryMock(user_id=DEVICE).create_disciplina(
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
        usecase = GetAllDisciplinasUsecase(DisciplinaRepositoryMock())
        response = usecase(device_id=DEVICE)
        assert len(response) == 5
        assert response[-1].code == "MIN001"
        assert response[-1].is_custom is True

    def test_get_all_disciplinas_usecase_empty_list(self):
        repository = DisciplinaRepositoryMock()
        repository.disciplinas = []
        usecase = GetAllDisciplinasUsecase(repository)

        with pytest.raises(NoItemsFound):
            usecase()
