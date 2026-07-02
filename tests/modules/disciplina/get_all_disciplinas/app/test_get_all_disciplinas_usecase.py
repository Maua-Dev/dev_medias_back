import pytest

from src.modules.disciplina.get_all_disciplinas.app.get_all_disciplinas_usecase import GetAllDisciplinasUsecase
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.disciplina_repository_mock import DisciplinaRepositoryMock


class TestGetAllDisciplinasUsecase:
    def test_get_all_disciplinas_usecase_success(self):
        repository = DisciplinaRepositoryMock()
        usecase = GetAllDisciplinasUsecase(repository)

        response = usecase()

        assert len(response) == 4
        assert response[0].code == "ECM101"

    def test_get_all_disciplinas_usecase_empty_list(self):
        repository = DisciplinaRepositoryMock()
        repository.disciplinas = []
        usecase = GetAllDisciplinasUsecase(repository)

        with pytest.raises(NoItemsFound):
            usecase()
