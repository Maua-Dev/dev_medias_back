import pytest
from unittest.mock import MagicMock
from src.modules.genetic_algorithm.app.genetic_algorithm_controller import GeneticAlgorithmController
from src.modules.genetic_algorithm.app.genetic_algorithm_usecase import GeneticAlgorithmUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest

class TestGeneticAlgorithmController:

    # ==========================================
    # TESTES DE SUCESSO (STATUS 200)
    # ==========================================

    def test_genetic_algorithm_controller_only_tests(self):
        request = HttpRequest(body={
            'provas_que_tenho': [{'valor': 5.0, 'peso': 0.5}],
            'trabalhos_que_tenho': [],
            'provas_que_quero': [{'peso': 0.5}],
            'trabalhos_que_quero': [],
            'peso_prova': 1.0,
            'peso_trabalho': 0.0,
            'media_desejada': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 200

    def test_genetic_algorithm_controller_only_assignments(self):
        request = HttpRequest(body={
            'provas_que_tenho': [],
            'trabalhos_que_tenho': [{'valor': 8.0, 'peso': 0.2}, {'valor': 9.0, 'peso': 0.2}],
            'provas_que_quero': [],
            'trabalhos_que_quero': [{'peso': 0.3}, {'peso': 0.3}],
            'peso_prova': 0.0,
            'peso_trabalho': 1.0,
            'media_desejada': 6.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 200

    # ==========================================
    # TESTES DE VALIDAÇÃO: provas_que_tenho
    # ==========================================

    def test_genetic_algorithm_controller_provas_que_tenho_missing(self):
        request = HttpRequest(body={
            'trabalhos_que_tenho': [],
            'provas_que_quero': [],
            'trabalhos_que_quero': [],
            'peso_prova': 0.6,
            'peso_trabalho': 0.4,
            'media_desejada': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro provas_que_tenho não existe'

    def test_genetic_algorithm_controller_provas_que_tenho_wrong_type(self):
        request = HttpRequest(body={
            'provas_que_tenho': 5.0,
            'trabalhos_que_tenho': [],
            'provas_que_quero': [],
            'trabalhos_que_quero': [],
            'peso_prova': 0.6,
            'peso_trabalho': 0.4,
            'media_desejada': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert 'Parâmetro provas_que_tenho não possui tipo correto' in response.body

    def test_genetic_algorithm_controller_provas_que_tenho_item_valor_wrong_type(self):
        request = HttpRequest(body={
            'provas_que_tenho': [{'valor': '6.0', 'peso': 0.5}],
            'trabalhos_que_tenho': [],
            'provas_que_quero': [],
            'trabalhos_que_quero': [],
            'peso_prova': 0.6,
            'peso_trabalho': 0.4,
            'media_desejada': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert 'Parâmetro provas_que_tenho item não possui tipo correto' in response.body

    def test_genetic_algorithm_controller_provas_que_tenho_peso_out_of_range(self):
        request = HttpRequest(body={
            'provas_que_tenho': [{'valor': 6.0, 'peso': 1.5}],
            'trabalhos_que_tenho': [],
            'provas_que_quero': [],
            'trabalhos_que_quero': [],
            'peso_prova': 0.6,
            'peso_trabalho': 0.4,
            'media_desejada': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert 'Must be between 0 and 1' in response.body

    # ==========================================
    # TESTES DE VALIDAÇÃO: trabalhos_que_tenho
    # ==========================================

    def test_genetic_algorithm_controller_trabalhos_que_tenho_missing(self):
        request = HttpRequest(body={
            'provas_que_tenho': [],
            'provas_que_quero': [],
            'trabalhos_que_quero': [],
            'peso_prova': 0.6,
            'peso_trabalho': 0.4,
            'media_desejada': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro trabalhos_que_tenho não existe'

    # ==========================================
    # TESTES DE VALIDAÇÃO: provas_que_quero
    # ==========================================

    def test_genetic_algorithm_controller_provas_que_quero_missing(self):
        request = HttpRequest(body={
            'provas_que_tenho': [],
            'trabalhos_que_tenho': [],
            'trabalhos_que_quero': [],
            'peso_prova': 0.6,
            'peso_trabalho': 0.4,
            'media_desejada': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro provas_que_quero não existe'

    # ==========================================
    # TESTES DE VALIDAÇÃO: trabalhos_que_quero
    # ==========================================

    def test_genetic_algorithm_controller_trabalhos_que_quero_missing(self):
        request = HttpRequest(body={
            'provas_que_tenho': [],
            'trabalhos_que_tenho': [],
            'provas_que_quero': [],
            'peso_prova': 0.6,
            'peso_trabalho': 0.4,
            'media_desejada': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro trabalhos_que_quero não existe'

    # ==========================================
    # TESTES DE VALIDAÇÃO: peso_prova, peso_trabalho e soma
    # ==========================================

    def test_genetic_algorithm_controller_peso_prova_missing(self):
        request = HttpRequest(body={
            'provas_que_tenho': [],
            'trabalhos_que_tenho': [],
            'provas_que_quero': [],
            'trabalhos_que_quero': [],
            'peso_trabalho': 0.4,
            'media_desejada': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro peso_prova não existe'

    def test_genetic_algorithm_controller_peso_prova_wrong_type(self):
        request = HttpRequest(body={
            'provas_que_tenho': [],
            'trabalhos_que_tenho': [],
            'provas_que_quero': [],
            'trabalhos_que_quero': [],
            'peso_prova': '0.6',
            'peso_trabalho': 0.4,
            'media_desejada': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert 'Parâmetro peso_prova não possui tipo correto' in response.body

    def test_genetic_algorithm_controller_pesos_sum_not_one(self):
        request = HttpRequest(body={
            'provas_que_tenho': [],
            'trabalhos_que_tenho': [],
            'provas_que_quero': [],
            'trabalhos_que_quero': [],
            'peso_prova': 0.8,
            'peso_trabalho': 0.4, # Soma = 1.2
            'media_desejada': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert 'Must sum 1.0' in response.body

    # ==========================================
    # TESTES DE VALIDAÇÃO: media_desejada
    # ==========================================

    def test_genetic_algorithm_controller_media_desejada_missing(self):
        request = HttpRequest(body={
            'provas_que_tenho': [],
            'trabalhos_que_tenho': [],
            'provas_que_quero': [],
            'trabalhos_que_quero': [],
            'peso_prova': 0.6,
            'peso_trabalho': 0.4
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro media_desejada não existe'

    def test_genetic_algorithm_controller_media_desejada_out_of_range(self):
        request = HttpRequest(body={
            'provas_que_tenho': [],
            'trabalhos_que_tenho': [],
            'provas_que_quero': [],
            'trabalhos_que_quero': [],
            'peso_prova': 0.6,
            'peso_trabalho': 0.4,
            'media_desejada': 11.0 # Fora do range 0-10
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert 'Must be between 0 and 10' in response.body