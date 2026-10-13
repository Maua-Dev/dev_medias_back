from unittest.mock import MagicMock

from src.modules.curso.create_curso.app.create_curso_controller import CreateCursoController
from src.modules.curso.create_curso.app.create_curso_usecase import CreateCursoUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.curso_repository_mock import CursoRepositoryMock


class TestCreateCursoController:
    def test_create_curso_controller_success(self):
        request = HttpRequest(body={'código': 'MAT', 'nome': 'Matemática'})
        usecase = CreateCursoUsecase(repository=CursoRepositoryMock())
        controller = CreateCursoController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 201
        assert response.body['código'] == 'MAT'
        assert response.body['nome'] == 'Matemática'

    def test_create_curso_controller_missing_codigo(self):
        request = HttpRequest(body={'nome': 'Matemática'})
        usecase = CreateCursoUsecase(repository=CursoRepositoryMock())
        controller = CreateCursoController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro código não existe'

    def test_create_curso_controller_wrong_codigo_type(self):
        request = HttpRequest(body={'código': 123, 'nome': 'Matemática'})
        usecase = CreateCursoUsecase(repository=CursoRepositoryMock())
        controller = CreateCursoController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro código não possui tipo correto.\n Recebido: int.\n Esperado: str'

    def test_create_curso_controller_missing_nome(self):
        request = HttpRequest(body={'código': 'MAT'})
        usecase = CreateCursoUsecase(repository=CursoRepositoryMock())
        controller = CreateCursoController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro nome não existe'

    def test_create_curso_controller_wrong_nome_type(self):
        request = HttpRequest(body={'código': 'MAT', 'nome': 123})
        usecase = CreateCursoUsecase(repository=CursoRepositoryMock())
        controller = CreateCursoController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro nome não possui tipo correto.\n Recebido: int.\n Esperado: str'

    def test_create_curso_controller_conflict(self):
        request = HttpRequest(body={'código': 'ECM', 'nome': 'Engenharia de Computação'})
        usecase = CreateCursoUsecase(repository=CursoRepositoryMock())
        controller = CreateCursoController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 409
        assert 'The item alredy exists for this código' in str(response.body)

    def test_create_curso_controller_internal_server_error(self):
        request = HttpRequest(body={'código': 'MAT', 'nome': 'Matemática'})
        usecase = MagicMock(side_effect=Exception('unexpected failure'))
        controller = CreateCursoController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 500
        assert str(response.body) == 'unexpected failure'
