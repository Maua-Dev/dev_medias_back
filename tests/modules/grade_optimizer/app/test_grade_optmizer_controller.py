import pytest
from src.modules.grade_optmizer.app.genetic_algorithm_controller import GeneticAlgorithmController
from src.modules.grade_optmizer.app.genetic_algorithm_usecase import GeneticAlgorithmUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest


class TestGeneticAlgorithmController:

    def test_possible_grade_controller_1(self):
        request = HttpRequest(body={
            "provas_que_tenho":[
                {"valor":6.0, "peso":0.25}
            ],
            "trabalhos_que_tenho":[
                {"valor":6.0, "peso":0.25},
                {"valor":6.0, "peso":0.25},
            ],
            "provas_que_quero":[
                {"valor":None, "peso":0.25},
                {"valor":None, "peso":0.25},
                {"valor":None, "peso":0.25},
            ],
            "trabalhos_que_quero":[
                {"valor":None, "peso":0.25},
                {"valor":None, "peso":0.25}
            ],
            "peso_prova":0.4,
            "peso_trabalho":0.6,
            "media_desejada":6
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body["message"] == "O algoritmo retornou uma combinação válida de notas"

    def test_possible_grade_controller_provas_que_tenho_nao_existe(self):
        request = HttpRequest(body={
            'trabalhos_que_tenho':[
                {'valor':6.0, 'peso':0.08},
                {'valor':6.0, 'peso':0.08},
            ],
            'provas_que_quero':[
                {'valor':None, 'peso':0.12},
                {'valor':None, 'peso':0.18},
                {'valor':None, 'peso':0.18},
            ],
            'trabalhos_que_quero':[
                {'valor':None, 'peso':0.12},
                {'valor':None, 'peso':0.12}
            ],
            'media_desejada':6
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert "Field provas_que_tenho is missing" in notas_resp.body

    def test_possible_grade_controller_provas_que_tenho_nao_e_lista(self):
        request = HttpRequest(body={
            'provas_que_tenho': {'valor':6.0, 'peso':0.12},
            'trabalhos_que_tenho': [{'valor':6.0, 'peso':0.08}],
            'provas_que_quero': [{'valor':None, 'peso':0.12}],
            'trabalhos_que_quero': [{'valor':None, 'peso':0.12}],
            'peso_prova':0.5,
            'peso_trabalho':0.5,
            'media_desejada':6
        })
        
        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert "isn't in the right type" in notas_resp.body
        assert "Expected: list" in notas_resp.body

    def test_possible_grade_controller_provas_que_tenho_peso_nao_e_float(self):
        request = HttpRequest(body={
            "provas_que_tenho":[
                {"valor": 1.0, "peso":"0.06"}
            ],
            "trabalhos_que_tenho":[],
            "provas_que_quero":[],
            "trabalhos_que_quero":[],
            "peso_prova": 1.0,
            "peso_trabalho": 0.0,
            "media_desejada":6
        })
        
        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert "isn't in the right type" in notas_resp.body
        
    def test_possible_grade_controller_invalid_input_media_desejada(self):
        request = HttpRequest(body={
            'provas_que_tenho':[{'valor':6.0, 'peso':0.12}],
            'trabalhos_que_tenho':[{'valor':6.0, 'peso':0.08}],
            'provas_que_quero':[{'valor':None, 'peso':0.12}],
            'trabalhos_que_quero':[{'valor':None, 'peso':0.12}],
            'peso_prova':0.6,
            'peso_trabalho':0.4,
            'media_desejada':16.2
        })
        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert "Must be between 0 and 10" in notas_resp.body
    
    def test_possible_grade_controller_function_input_error(self):
        request = HttpRequest(body={
            'provas_que_tenho': [{'valor':6.0, 'peso':0.2}],
            'trabalhos_que_tenho': [{'valor':6.0, 'peso':0.2}],
            'provas_que_quero': [{'valor':None, 'peso':0.2}],
            'trabalhos_que_quero': [{'valor':None, 'peso':0.3}],
            'peso_prova':0.7, # A soma de 0.7 e 0.4 não é 1
            'peso_trabalho':0.4,
            'media_desejada':6
        })
        
        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert "Must sum 1.0" in notas_resp.body