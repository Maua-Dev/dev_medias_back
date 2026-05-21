from src.modules.curso.get_all_cursos.app.get_all_cursos_viewmodel import GetAllCursosViewmodel
from src.shared.infra.repositories.curso_repository_mock import CursoRepositoryMock


class TestGetAllCursosViewmodel:
    def test_to_dict_returns_list(self):
        cursos = CursoRepositoryMock().get_all_cursos()

        response = GetAllCursosViewmodel(cursos).to_dict()

        assert isinstance(response, list)
        assert len(response) == 3

    def test_to_dict_contains_expected_fields(self):
        cursos = CursoRepositoryMock().get_all_cursos()

        response = GetAllCursosViewmodel(cursos).to_dict()

        assert response[0]['código'] == 'ECM'
        assert response[0]['nome'] == 'Engenharia de Computação'
