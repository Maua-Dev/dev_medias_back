import json
from src.modules.grade_optmizer.app.genetic_algorithm_presenter import lambda_handler


class Test_GeneticAlgorithmPresenter:
    def test_grade_optmizer_presenter(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "requestContext": {
                "http": {
                    "method": "POST"
                }
            },
            "body": {
                'provas_que_tenho': [{'valor':6.0, 'peso':0.2}],
                'trabalhos_que_tenho': [{'valor':6.0, 'peso':0.2}, {'valor':6.0, 'peso':0.2}],
                'provas_que_quero': [{'valor':None, 'peso':0.2}, {'valor':None, 'peso':0.3}, {'valor':None, 'peso':0.3}],
                'trabalhos_que_quero': [{'valor':None, 'peso':0.3}, {'valor':None, 'peso':0.3}],
                'peso_prova':0.4,
                'peso_trabalho':0.6,
                'media_desejada':6
            }
        }

        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 200
        assert json.loads(response["body"])["message"] == "O algoritmo retornou uma combinação válida de notas"
        
    def test_grade_optmizer_presenter_not_found(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "requestContext": {
                "http": {
                    "method": "POST"
                }
            },
            "body": {
                'provas_que_tenho': [{'valor':6.0, 'peso':0.2}],
                'trabalhos_que_tenho': [{'valor':6.0, 'peso':0.2}, {'valor':6.0, 'peso':0.2}],
                'provas_que_quero': [{'valor':None, 'peso':0.2}, {'valor':None, 'peso':0.3}, {'valor':None, 'peso':0.3}],
                'trabalhos_que_quero': [{'valor':None, 'peso':0.3}, {'valor':None, 'peso':0.3}],
                'peso_prova':0.4,
                'peso_trabalho':0.6,
                'media_desejada':9.9 # Muito alto, causa CombinationNotFound
            }
        }

        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 404
        assert "combinação" in json.loads(response["body"])
        
    def test_grade_optmizer_presenter_bad_request(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "requestContext": {
                "http": {
                    "method": "POST"
                }
            },
            "body": {
                'provas_que_tenho': [{'valor':6.0, 'peso':0.2}],
                'trabalhos_que_tenho': [{'valor':6.0, 'peso':0.2}],
                'provas_que_quero': [{'valor':None, 'peso':0.2}],
                'trabalhos_que_quero': [{'valor':None, 'peso':0.3}],
                'peso_prova':0.8, # Errado nam matemática, não soma 1.0 com 0.6
                'peso_trabalho':0.6,
                'media_desejada':6
            }
        }

        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 400
        assert "Must sum 1.0" in json.loads(response["body"])