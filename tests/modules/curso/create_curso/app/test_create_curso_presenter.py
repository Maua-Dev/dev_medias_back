import json
import os


class TestCreateCursoPresenter:
    def test_lambda_handler_success(self):
        previous_stage = os.environ.get('STAGE')
        os.environ['STAGE'] = 'TEST'
        from src.modules.curso.create_curso.app.create_curso_presenter import lambda_handler

        event = {
            'version': '2.0',
            'routeKey': '$default',
            'rawPath': '/cursos',
            'rawQueryString': '',
            'headers': {},
            'queryStringParameters': None,
            'requestContext': {},
            'body': {
                'código': 'MAT',
                'nome': 'Matemática',
            },
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

        assert response['statusCode'] == 201
        body = json.loads(response['body'])
        assert body['código'] == 'MAT'
        assert body['nome'] == 'Matemática'
