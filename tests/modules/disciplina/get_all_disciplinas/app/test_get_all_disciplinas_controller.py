from unittest.mock import MagicMock

from src.modules.disciplina.get_all_disciplinas.app.get_all_disciplinas_controller import GetAllDisciplinasController
from src.modules.disciplina.get_all_disciplinas.app.get_all_disciplinas_usecase import GetAllDisciplinasUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.infra.repositories.disciplina_repository_mock import DisciplinaRepositoryMock


class TestGetAllDisciplinasController:
    def test_get_all_disciplinas_controller_success(self):
        request = HttpRequest()
        usecase = GetAllDisciplinasUsecase(repository=DisciplinaRepositoryMock())
        controller = GetAllDisciplinasController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 200
        assert isinstance(response.body, list)
        assert response.body[0]["code"] == "ECM101"

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
        request = HttpRequest()
        usecase = MagicMock(side_effect=Exception("unexpected failure"))
        controller = GetAllDisciplinasController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 500
        assert str(response.body) == "unexpected failure"
