import json
import os

from src.modules.disciplina.get_all_disciplinas.app.get_all_disciplinas_presenter import lambda_handler


class TestGetAllDisciplinasPresenter:
    def test_lambda_handler_success(self):
        previous_stage = os.environ.get("STAGE")
        os.environ["STAGE"] = "TEST"
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/disciplinas",
            "rawQueryString": "",
            "headers": {},
            "queryStringParameters": None,
            "requestContext": {},
            "body": {},
            "pathParameters": None,
            "isBase64Encoded": False,
            "stageVariables": None,
        }

        try:
            response = lambda_handler(event=event, context=None)
        finally:
            if previous_stage is None:
                os.environ.pop("STAGE", None)
            else:
                os.environ["STAGE"] = previous_stage

        assert response["statusCode"] == 200
        body = json.loads(response["body"])
        assert isinstance(body, list)
        assert len(body) == 4
        assert body[0]["code"] == "ECM101"
