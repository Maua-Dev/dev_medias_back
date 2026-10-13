from unittest.mock import MagicMock

from src.modules.curso.get_all_cursos.app.get_all_cursos_controller import GetAllCursosController
from src.modules.curso.get_all_cursos.app.get_all_cursos_usecase import GetAllCursosUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.curso_repository_mock import CursoRepositoryMock


class TestGetAllCursosController:
    def test_get_all_cursos_controller_success(self):
        request = HttpRequest()
        usecase = GetAllCursosUsecase(repository=CursoRepositoryMock())
        controller = GetAllCursosController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 200
        assert isinstance(response.body, list)
        assert response.body[0]['código'] == 'ECM'

    def test_get_all_cursos_controller_not_found(self):
        request = HttpRequest()
        repository = CursoRepositoryMock()
        repository.cursos = []
        usecase = GetAllCursosUsecase(repository=repository)
        controller = GetAllCursosController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 404
        assert 'No items found for cursos' in str(response.body)

    def test_get_all_cursos_controller_internal_server_error(self):
        request = HttpRequest()
        usecase = MagicMock(side_effect=Exception('unexpected failure'))
        controller = GetAllCursosController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 500
        assert str(response.body) == 'unexpected failure'
