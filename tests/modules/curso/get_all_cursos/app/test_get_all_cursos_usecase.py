import pytest

from src.modules.curso.get_all_cursos.app.get_all_cursos_usecase import GetAllCursosUsecase
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.infra.repositories.curso_repository_mock import CursoRepositoryMock


class TestGetAllCursosUsecase:
    def test_get_all_cursos_usecase_success(self):
        repository = CursoRepositoryMock()
        usecase = GetAllCursosUsecase(repository)

        response = usecase()

        assert len(response) == 3
        assert response[0].código == 'ECM'

    def test_get_all_cursos_usecase_empty_list(self):
        repository = CursoRepositoryMock()
        repository.cursos = []
        usecase = GetAllCursosUsecase(repository)

        with pytest.raises(NoItemsFound):
            usecase()
