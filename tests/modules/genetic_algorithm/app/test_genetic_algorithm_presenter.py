# tests/modules/genetic_algorithm/app/test_genetic_algorithm_presenter.py

import json
from src.modules.genetic_algorithm.app.genetic_algorithm_presenter import lambda_handler


class TestGeneticAlgorithmPresenter:

    def _make_event(self, body):
        return {"body": body}

    def _default_body(self, **kwargs):
        body = {
            'provas_que_tenho': [{'valor': 6.0, 'peso': 0.25}, {'valor': 7.0, 'peso': 0.25}],
            'trabalhos_que_tenho': [{'valor': 8.0, 'peso': 0.5}],
            'provas_que_quero': [{'peso': 0.25}, {'peso': 0.25}],
            'trabalhos_que_quero': [{'peso': 0.5}],
            'peso_prova': 0.6,
            'peso_trabalho': 0.4,
            'media_desejada': 7.0,
        }
        body.update(kwargs)
        return body
    # ==========================================
    # Sucesso
    # ==========================================

    def test_success_basic(self):
        response = lambda_handler(event=self._make_event(self._default_body()), context=None)
        assert response["statusCode"] == 200

    def test_success_only_tests(self):
        body = {
            'provas_que_tenho': [{'valor': 5.0, 'peso': 0.5}],
            'trabalhos_que_tenho': [],
            'provas_que_quero': [{'peso': 0.25}, {'peso': 0.25}],  # 0.5 + 0.25 + 0.25 = 1.0
            'trabalhos_que_quero': [],
            'peso_prova': 1.0,
            'peso_trabalho': 0.0,
            'media_desejada': 7.0,
        }
        response = lambda_handler(event=self._make_event(body), context=None)
        assert response["statusCode"] == 200

    def test_success_only_assignments(self):
        body = {
            'provas_que_tenho': [],
            'trabalhos_que_tenho': [{'valor': 8.0, 'peso': 0.25}, {'valor': 9.0, 'peso': 0.25}],
            'provas_que_quero': [],
            'trabalhos_que_quero': [{'peso': 0.25}, {'peso': 0.25}],  # soma 1.0
            'peso_prova': 0.0,
            'peso_trabalho': 1.0,
            'media_desejada': 6.0,
        }
        response = lambda_handler(event=self._make_event(body), context=None)
        assert response["statusCode"] == 200

    def test_success_high_target(self):
        body = self._default_body(
            provas_que_tenho=[{'valor': 10.0, 'peso': 0.5}],
            trabalhos_que_tenho=[{'valor': 10.0, 'peso': 0.5}],
            media_desejada=10.0
        )
        response = lambda_handler(event=self._make_event(body), context=None)
        assert response["statusCode"] == 200

    def test_success_low_target(self):
        response = lambda_handler(event=self._make_event(self._default_body(media_desejada=1.0)), context=None)
        assert response["statusCode"] == 200

    def test_success_response_has_expected_keys(self):
        response = lambda_handler(event=self._make_event(self._default_body()), context=None)
        body = json.loads(response["body"])
        for key in ["tests", "assignments", "final_average", "target_average"]:
            assert key in body

    def test_success_multiple_calls(self):
        for _ in range(5):
            response = lambda_handler(event=self._make_event(self._default_body()), context=None)
            assert response["statusCode"] == 200

    # ==========================================
    # Parâmetros faltando
    # ==========================================

    def test_missing_provas_que_tenho(self):
        body = self._default_body()
        del body['provas_que_tenho']
        response = lambda_handler(event=self._make_event(body), context=None)
        assert response["statusCode"] == 400
        assert 'provas_que_tenho' in json.loads(response["body"])

    def test_missing_trabalhos_que_tenho(self):
        body = self._default_body()
        del body['trabalhos_que_tenho']
        response = lambda_handler(event=self._make_event(body), context=None)
        assert response["statusCode"] == 400
        assert 'trabalhos_que_tenho' in json.loads(response["body"])

    def test_missing_provas_que_quero(self):
        body = self._default_body()
        del body['provas_que_quero']
        response = lambda_handler(event=self._make_event(body), context=None)
        assert response["statusCode"] == 400
        assert 'provas_que_quero' in json.loads(response["body"])

    def test_missing_trabalhos_que_quero(self):
        body = self._default_body()
        del body['trabalhos_que_quero']
        response = lambda_handler(event=self._make_event(body), context=None)
        assert response["statusCode"] == 400
        assert 'trabalhos_que_quero' in json.loads(response["body"])

    def test_missing_peso_prova(self):
        body = self._default_body()
        del body['peso_prova']
        response = lambda_handler(event=self._make_event(body), context=None)
        assert response["statusCode"] == 400
        assert 'peso_prova' in json.loads(response["body"])

    def test_missing_peso_trabalho(self):
        body = self._default_body()
        del body['peso_trabalho']
        response = lambda_handler(event=self._make_event(body), context=None)
        assert response["statusCode"] == 400
        assert 'peso_trabalho' in json.loads(response["body"])

    def test_missing_media_desejada(self):
        body = self._default_body()
        del body['media_desejada']
        response = lambda_handler(event=self._make_event(body), context=None)
        assert response["statusCode"] == 400
        assert 'media_desejada' in json.loads(response["body"])

    # ==========================================
    # Tipos errados
    # ==========================================

    def test_wrong_type_provas_que_tenho(self):
        response = lambda_handler(event=self._make_event(self._default_body(provas_que_tenho=6.0)), context=None)
        assert response["statusCode"] == 400
        assert 'provas_que_tenho' in json.loads(response["body"])

    def test_wrong_type_peso_prova(self):
        response = lambda_handler(event=self._make_event(self._default_body(peso_prova='0.6')), context=None)
        assert response["statusCode"] == 400
        assert 'peso_prova' in json.loads(response["body"])

    def test_wrong_type_media_desejada(self):
        response = lambda_handler(event=self._make_event(self._default_body(media_desejada='7.0')), context=None)
        assert response["statusCode"] == 400
        assert 'media_desejada' in json.loads(response["body"])

    def test_wrong_type_nota_valor(self):
        body = self._default_body(provas_que_tenho=[{'valor': 'seis', 'peso': 1.0}])
        response = lambda_handler(event=self._make_event(body), context=None)
        assert response["statusCode"] == 400

    def test_wrong_type_nota_peso(self):
        body = self._default_body(provas_que_tenho=[{'valor': 6.0, 'peso': 'alto'}])
        response = lambda_handler(event=self._make_event(body), context=None)
        assert response["statusCode"] == 400

    # ==========================================
    # Valores fora do range
    # ==========================================

    def test_peso_prova_out_of_range(self):
        response = lambda_handler(event=self._make_event(self._default_body(peso_prova=1.5, peso_trabalho=0.4)), context=None)
        assert response["statusCode"] == 400

    def test_media_desejada_out_of_range(self):
        response = lambda_handler(event=self._make_event(self._default_body(media_desejada=15.0)), context=None)
        assert response["statusCode"] == 400

    def test_nota_peso_out_of_range(self):
        body = self._default_body(provas_que_tenho=[{'valor': 6.0, 'peso': 1.5}])
        response = lambda_handler(event=self._make_event(body), context=None)
        assert response["statusCode"] == 400

    def test_pesos_nao_somam_um(self):
        response = lambda_handler(event=self._make_event(self._default_body(peso_prova=0.5, peso_trabalho=0.3)), context=None)
        assert response["statusCode"] == 400

    # ==========================================
    # Formato API Gateway (body como string JSON)
    # ==========================================

    def test_api_gateway_body_as_string(self):
        event = {
            'body': json.dumps(self._default_body()),
            'isBase64Encoded': False
        }
        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 200