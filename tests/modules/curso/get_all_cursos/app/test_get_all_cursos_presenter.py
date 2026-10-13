import json
import os


class TestGetAllCursosPresenter:
    def test_lambda_handler_success(self):
        previous_stage = os.environ.get('STAGE')
        os.environ['STAGE'] = 'TEST'
        from src.modules.curso.get_all_cursos.app.get_all_cursos_presenter import lambda_handler

        event = {
            'version': '2.0',
            'routeKey': '$default',
            'rawPath': '/cursos',
            'rawQueryString': '',
            'headers': {},
            'queryStringParameters': None,
            'requestContext': {},
            'body': {},
            'pathParameters': None,
            'isBase64Encoded': False,
            'stageVariables': None,
        }

        try:
            response = lambda_handler(event=event, context=None)
        finally:
            if previous_stage is None:
                os.environ.pop('STAGE', None)
            else:
                os.environ['STAGE'] = previous_stage

        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert isinstance(body, list)
        assert len(body) == 3
        assert body[0]['código'] == 'ECM'
