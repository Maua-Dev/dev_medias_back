import json

from src.modules.disciplina.get_all_disciplinas.app import get_all_disciplinas_presenter
from src.shared.helpers.external_interfaces.http_codes import NotFound, OK


class TestGetAllDisciplinasPresenter:
    def test_lambda_handler_success(self, monkeypatch):
        class ControllerStub:
            def __call__(self, request):
                return OK([{"code": "ECM101"}])

        monkeypatch.setattr(get_all_disciplinas_presenter, "controller", ControllerStub())

        response = get_all_disciplinas_presenter.lambda_handler(event={}, context=None)

        assert response["statusCode"] == 200
        assert json.loads(response["body"]) == [{"code": "ECM101"}]

    def test_lambda_handler_not_found(self, monkeypatch):
        class ControllerStub:
            def __call__(self, request):
                return NotFound("No items found for disciplinas")

        monkeypatch.setattr(get_all_disciplinas_presenter, "controller", ControllerStub())

        response = get_all_disciplinas_presenter.lambda_handler(event={}, context=None)

        assert response["statusCode"] == 404
        assert "No items found for disciplinas" in json.loads(response["body"])
