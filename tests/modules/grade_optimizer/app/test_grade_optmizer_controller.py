import pytest
from src.modules.grade_optmizer.app.grade_optmizer_controller import GradeOptmizerController

from src.modules.grade_optmizer.app.grade_optmizer_usecase import GradeOptimizerUsecase
from src.shared.domain.entities.nota import Nota
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.helpers.functions.utils import Utils
from src.shared.solucionador import Solucionador


class TestGradeOptimizerController:

    def test_possible_grade_controller(self):
        request = HttpRequest(body={
            'provas_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.12
                }
            ],
            'trabalhos_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'provas_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.18
                },
            ],
            'trabalhos_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6
        })

        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body["message"] == "O algoritmo retornou uma combinação válida de notas"

    def test_possible_grade_controller_provas_que_tenho_nao_existe(self):
        request = HttpRequest(body={
            'trabalhos_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'provas_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.18
                },
            ],
            'trabalhos_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6
        })

        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro provas_que_tenho não existe"
        
    def test_possible_grade_controller_provas_que_tenho_nao_e_lista(self):
        request = HttpRequest(body={
            'provas_que_tenho':
            {
                'valor':6.0,
                'peso':0.12
            },
            'trabalhos_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'provas_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.18
                },
            ],
            'trabalhos_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6
        })
        
        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro provas_que_tenho não possui tipo correto.\n Recebido: dict.\n Esperado: list"
        
    def test_possible_grade_controller_provas_que_tenho_nao_e_lista_de_dicionarios(self):
        request = HttpRequest(body={
            'provas_que_tenho':[6.0],
            'trabalhos_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'provas_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.18
                },
            ],
            'trabalhos_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6
        })
        
        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro provas_que_tenho não é válido"
        
    def test_possible_grade_controller_provas_que_tenho_nao_tem_valor(self):
        request = HttpRequest(body={
            'provas_que_tenho':[
                {
                    'peso':0.12
                }
            ],
            'trabalhos_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'provas_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.18
                },
            ],
            'trabalhos_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6
        })
        
        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro valor não é válido"
        
    def test_possible_grade_controller_provas_que_tenho_valor_nao_e_float(self):
        request = HttpRequest(body={
            'provas_que_tenho':[
                {
                    'valor': '1.0',
                    'peso':0.12
                }
            ],
            'trabalhos_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'provas_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.18
                },
            ],
            'trabalhos_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6
        })
        
        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Valor de nota 1.0 deve ser um número"
        
    def test_possible_grade_controller_provas_que_tenho_nao_tem_peso(self):
        request = HttpRequest(body={
            'provas_que_tenho':[
                {
                    'valor': 1.0,
                    'peso':0.06
                },
                {
                    'valor': 1.0,
                    'peso':None
                }
            ],
            'trabalhos_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'provas_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.18
                },
            ],
            'trabalhos_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6
        })
        
        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro peso não é válido"
        
    def test_possible_grade_controller_provas_que_tenho_peso_nao_e_float(self):
        request = HttpRequest(body={
            'provas_que_tenho':[
                {
                    'valor': 1.0,
                    'peso':0.06
                },
                {
                    'valor': 1.0,
                    'peso':'0.06'
                }
            ],
            'trabalhos_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'provas_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.18
                },
            ],
            'trabalhos_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6
        })
        
        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Peso 0.06 deve ser um número"
        
    def test_possible_grade_controller_trabalhos_que_tenho_nao_existe(self):
        request = HttpRequest(body={
            'provas_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'provas_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.18
                },
            ],
            'trabalhos_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6
        })

        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro trabalhos_que_tenho não existe"
        
    def test_possible_grade_controller_trabalhos_que_tenho_nao_e_lista(self):
        request = HttpRequest(body={
            'trabalhos_que_tenho':
            {
                'valor':6.0,
                'peso':0.12
            },
            'provas_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'provas_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.18
                },
            ],
            'trabalhos_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6
        })
        
        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro trabalhos_que_tenho não possui tipo correto.\n Recebido: dict.\n Esperado: list"
        
    def test_possible_grade_controller_trabalhos_que_tenho_nao_e_lista_de_dicionarios(self):
        request = HttpRequest(body={
            'trabalhos_que_tenho':[6.0],
            'provas_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'provas_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.18
                },
            ],
            'trabalhos_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6
        })
        
        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro trabalhos_que_tenho não é válido"
        
    def test_possible_grade_controller_trabalhos_que_tenho_nao_tem_valor(self):
        request = HttpRequest(body={
            'trabalhos_que_tenho':[
                {
                    'peso':0.12
                }
            ],
            'provas_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'provas_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.18
                },
            ],
            'trabalhos_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6
        })
        
        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro valor não é válido"
        
    def test_possible_grade_controller_trabalhos_que_tenho_valor_nao_e_float(self):
        request = HttpRequest(body={
            'trabalhos_que_tenho':[
                {
                    'valor': '1.0',
                    'peso':0.12
                }
            ],
            'provas_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'provas_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.18
                },
            ],
            'trabalhos_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6
        })
        
        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Valor de nota 1.0 deve ser um número"
        
    def test_possible_grade_controller_trabalhos_que_tenho_nao_tem_peso(self):
        request = HttpRequest(body={
            'trabalhos_que_tenho':[
                {
                    'valor': 1.0,
                    'peso':0.06
                },
                {
                    'valor': 1.0,
                    'peso':None
                }
            ],
            'provas_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'provas_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.18
                },
            ],
            'trabalhos_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6
        })
        
        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro peso não é válido"
        
    def test_possible_grade_controller_trabalhos_que_tenho_peso_nao_e_float(self):
        request = HttpRequest(body={
            'trabalhos_que_tenho':[
                {
                    'valor': 1.0,
                    'peso':0.06
                },
                {
                    'valor': 1.0,
                    'peso':'0.06'
                }
            ],
            'provas_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'provas_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.18
                },
            ],
            'trabalhos_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6
        })
        
        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Peso 0.06 deve ser um número"
        
    def test_possible_grade_controller_provas_que_quero_nao_existe(self):
        request = HttpRequest(body={
            'provas_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.12
                }
            ],
            'trabalhos_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'trabalhos_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6
        })

        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro provas_que_quero não existe"
        
    def test_possible_grade_controller_provas_que_quero_nao_e_lista(self):
        request = HttpRequest(body={
            'provas_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.12
                }
            ],
            'trabalhos_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'provas_que_quero':
            {
                'valor':None,
                'peso':0.18
            },
            'trabalhos_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6
        })

        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro provas_que_quero não possui tipo correto.\n Recebido: dict.\n Esperado: list"
        
    def test_possible_grade_controller_provas_que_quero_nao_sao_dicionarios(self):
        request = HttpRequest(body={
            'provas_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.12
                }
            ],
            'trabalhos_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'provas_que_quero':[1.0, 2.5, 4.0],
            'trabalhos_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6
        })
        
        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro provas_que_quero não é válido"
        
    def test_possible_grade_controller_provas_que_quero_tem_valor(self):
        request = HttpRequest(body={
            'provas_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.12
                }
            ],
            'trabalhos_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'provas_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':2.5,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.18
                },
            ],
            'trabalhos_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6
        })

        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro valor não é válido"
        
    def test_possible_grade_controller_provas_que_quero_nao_tem_peso(self):
        request = HttpRequest(body={
            'provas_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.12
                }
            ],
            'trabalhos_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'provas_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':None
                },
            ],
            'trabalhos_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6
        })

        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro peso não é válido"
        
    def test_possible_grade_controller_provas_que_quero_peso_nao_e_float(self):
        request = HttpRequest(body={
            'provas_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.12
                }
            ],
            'trabalhos_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'provas_que_quero':[
                {
                    'valor':None,
                    'peso':'0.12'
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.18
                },
            ],
            'trabalhos_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6
        })
        
        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Peso 0.12 deve ser um número"
        
    def test_possible_grade_controller_trabalhos_que_quero_nao_existe(self):
        request = HttpRequest(body={
            'provas_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.12
                }
            ],
            'trabalhos_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'provas_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6
        })

        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro trabalhos_que_quero não existe"
        
    def test_possible_grade_controller_trabalhos_que_quero_nao_e_lista(self):
        request = HttpRequest(body={
            'provas_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.12
                }
            ],
            'trabalhos_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'trabalhos_que_quero':
            {
                'valor':None,
                'peso':0.18
            },
            'provas_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6
        })

        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro trabalhos_que_quero não possui tipo correto.\n Recebido: dict.\n Esperado: list"
        
    def test_possible_grade_controller_trabalhos_que_quero_nao_sao_dicionarios(self):
        request = HttpRequest(body={
            'provas_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.12
                }
            ],
            'trabalhos_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'trabalhos_que_quero':[1.0, 2.5, 4.0],
            'provas_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6
        })
        
        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro trabalhos_que_quero não é válido"
        
    def test_possible_grade_controller_trabalhos_que_quero_tem_valor(self):
        request = HttpRequest(body={
            'provas_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.12
                }
            ],
            'trabalhos_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'provas_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':2.5,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.18
                },
            ],
            'trabalhos_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6
        })

        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro valor não é válido"
        
    def test_possible_grade_controller_trabalhos_que_quero_nao_tem_peso(self):
        request = HttpRequest(body={
            'provas_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.12
                }
            ],
            'trabalhos_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'trabalhos_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':None
                },
            ],
            'provas_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6
        })

        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro peso não é válido"
        
    def test_possible_grade_controller_trabalhos_que_quero_peso_nao_e_float(self):
        request = HttpRequest(body={
            'provas_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.12
                }
            ],
            'trabalhos_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'trabalhos_que_quero':[
                {
                    'valor':None,
                    'peso':'0.12'
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.18
                },
            ],
            'provas_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6
        })
        
        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Peso 0.12 deve ser um número"
        
    def test_possible_grade_controller_media_desejada_nao_e_float(self):
        request = HttpRequest(body={
            'provas_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.12
                }
            ],
            'trabalhos_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'provas_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.18
                },
            ],
            'trabalhos_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':'6'
        })
        
        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro media_desejada não possui tipo correto.\n Recebido: str.\n Esperado: float"

    def test_possible_grade_controller_invalid_input_notas_que_quero(self):
        request = HttpRequest(body={
            'provas_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.12
                }
            ],
            'trabalhos_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'provas_que_quero':[
            ],
            'trabalhos_que_quero':[
            ],
            'media_desejada':6
        })
        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro provas_que_quero e trabalhos_que_quero está(ão) inválido(s): Não podem ser listas vazias"
    
    def test_possible_grade_controller_invalid_input_media_desejada(self):
        request = HttpRequest(body={
            'provas_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.12
                }
            ],
            'trabalhos_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'provas_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.18
                },
            ],
            'trabalhos_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':16.2
        })
        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro media_desejada está(ão) inválido(s): Deve estar compreendida entre 0 e 10"
    
    def test_possible_grade_controller_function_input_error(self):
        request = HttpRequest(body={
            'provas_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.12
                }
            ],
            'trabalhos_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'provas_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.19
                },
                {
                    'valor':None,
                    'peso':0.18
                },
            ],
            'trabalhos_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6
        })
        
        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "A soma dos pesos das notas passadas deve ser 1"
        
    def test_possible_grade_controller_entity_parameter_error(self):
        request = HttpRequest(body={
            'provas_que_tenho':[
                {
                    'valor':6.1,
                    'peso':0.12
                }
            ],
            'trabalhos_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'provas_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.18
                },
            ],
            'trabalhos_que_quero':[
                {
                    'valor':None,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6
        })
        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Valor de nota 6.1 deve estar entre 0 e 10, variando de 0.5 em 0.5"
        
    