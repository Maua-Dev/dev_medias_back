import pytest
from src.modules.grade_optimizer.app.grade_optmizer_controller import GradeOptmizerController

from src.modules.grade_optimizer.app.grade_optmizer_usecase import GradeOptimizerUsecase
from src.shared.domain.entities.nota import Nota
from src.shared.helpers.external_interfaces.http_models import HttpRequest
from src.shared.helpers.functions.utils import Utils
from src.shared.solucionador import Solucionador


class TestGradeOptimizerController:

    def test_possible_grade_controller(self):
        request = HttpRequest(body={
            'notas_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.12
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'notas_que_quero':[
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
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6.0
        })

        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 200
        assert notas_resp.body["message"] == "o algoritmo retonrou uma combinação válida de notas"

    def test_possible_grade_controller_notas_que_tenho_nao_existe(self):
        request = HttpRequest(body={
            'notas_que_quero':[
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
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6.0
        })

        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro notas_que_tenho não existe"
        
    def test_possible_grade_controller_notas_que_tenho_nao_e_lista(self):
        request = HttpRequest(body={
            'notas_que_tenho':{},
            'notas_que_quero':[
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
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6.0
        })
        
        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro notas_que_tenho não possui tipo correto.\n Recebido: NoneType.\n Esperado: list"
        
    def test_possible_grade_controller_notas_que_tenho_nao_sao_dicionarios(self):
        request = HttpRequest(body={
            'notas_que_tenho':[1.0, 2.0, 3.0],
            'notas_que_quero':[
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
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6.0
        })
        
        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro notas_que_tenho não é válido"
        
    def test_possible_grade_controller_notas_que_tenho_nao_tem_valor(self):
        request = HttpRequest(body={
            'notas_que_tenho':[
                {
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'notas_que_quero':[
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
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6.0
        })
        
        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro valor não é válido"
        
    def test_possible_grade_controller_notas_que_tenho_valor_nao_e_float(self):
        request = HttpRequest(body={
            'notas_que_tenho':[
                {
                    'valor':'1.0',
                    'peso':0.12
                },
                {
                    'valor':'1.0',
                    'peso':0.18
                },
                {
                    'valor':'1.0',
                    'peso':0.12
                }
            ],
            'notas_que_quero':[
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
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6.0
        })
        
        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Valor de nota 1.0 deve ser um número"
        
    def test_possible_grade_controller_notas_que_tenho_nao_tem_peso(self):
        request = HttpRequest(body={
            'notas_que_tenho':[
                {
                    'valor':1.0,
                    'peso':0.12
                },
                {
                    'valor':1.0,
                    'peso':None
                },
                {
                    'valor':1.0,
                    'peso':0.12
                }
            ],
            'notas_que_quero':[
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
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6.0
        })
        
        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro peso não é válido"
        
    def test_possible_grade_controller_notas_que_tenho_peso_nao_e_float(self):
        request = HttpRequest(body={
            'notas_que_tenho':[
                {
                    'valor':1.0,
                    'peso':0.12
                },
                {
                    'valor':1.0,
                    'peso':'0.23'
                },
                {
                    'valor':1.0,
                    'peso':0.12
                }
            ],
            'notas_que_quero':[
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
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6.0
        })
        
        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Peso 0.23 deve ser um número"
        
    def test_possible_grade_controller_notas_que_quero_nao_existe(self):
        request = HttpRequest(body={
            'notas_que_tenho':[
                {
                    'valor':1.0,
                    'peso':0.12
                },
                {
                    'valor':2.0,
                    'peso':0.18
                },
                {
                    'valor':2.0,
                    'peso':0.12
                },
                {
                    'valor':2.0,
                    'peso':0.18
                },
                {
                    'valor':10.0,
                    'peso':0.12
                }
            ],
            'media_desejada':6.0
        })

        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro notas_que_quero não existe"
        
    def test_possible_grade_controller_notas_que_quero_nao_e_lista(self):
        request = HttpRequest(body={
            'notas_que_tenho':[
                {
                    'valor':1.0,
                    'peso':0.12
                },
                {
                    'valor':2.0,
                    'peso':0.18
                },
                {
                    'valor':2.0,
                    'peso':0.12
                },
                {
                    'valor':2.0,
                    'peso':0.18
                },
                {
                    'valor':10.0,
                    'peso':0.12
                }
            ],
            'notas_que_quero':{
                'valor':None,
                'peso':0.12
            },
            'media_desejada':6.0
        })

        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro notas_que_quero não possui tipo correto.\n Recebido: NoneType.\n Esperado: list"
        
    def test_possible_grade_controller_notas_que_quero_nao_sao_dicionarios(self):
        request = HttpRequest(body={
            'notas_que_quero':[1.0, 2.0, 3.0],
            'notas_que_tenho':[
                {
                    'valor':1.0,
                    'peso':0.12
                },
                {
                    'valor':1.0,
                    'peso':0.18
                },
                {
                    'valor':1.0,
                    'peso':0.12
                },
                {
                    'valor':1.0,
                    'peso':0.18
                },
                {
                    'valor':1.0,
                    'peso':0.12
                }
            ],
            'media_desejada':6.0
        })
        
        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro notas_que_quero não é válido"
        
    def test_possible_grade_controller_notas_que_quero_tem_valor(self):
        request = HttpRequest(body={
            'notas_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.12
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'notas_que_quero':[
                {
                    'valor':6.0,
                    'peso':0.12
                },
                {
                    'valor':None,
                    'peso':0.18
                },
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
                    'peso':0.12
                }
            ],
            'media_desejada':6.0
        })

        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro valor não é válido"
        
    def test_possible_grade_controller_notas_que_quero_nao_tem_peso(self):
        request = HttpRequest(body={
            'notas_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.12
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
                {
                    'valor':6.0,
                    'peso':0.08
                },
            ],
            'notas_que_quero':[
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
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6.0
        })

        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Parâmetro peso não é válido"
        
    def test_possible_grade_controller_notas_que_quero_peso_nao_e_float(self):
        request = HttpRequest(body={
            'notas_que_tenho':[
                {
                    'valor':1.0,
                    'peso':0.12
                },
                {
                    'valor':1.0,
                    'peso':0.18
                },
                {
                    'valor':1.0,
                    'peso':0.12
                }
            ],
            'notas_que_quero':[
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
                    'peso':'a'
                },
                {
                    'valor':None,
                    'peso':0.18
                },
                {
                    'valor':None,
                    'peso':0.12
                }
            ],
            'media_desejada':6.0
        })
        
        usecase = GradeOptimizerUsecase()
        controller = GradeOptmizerController(usecase=usecase)

        notas_resp = controller(request=request)

        assert notas_resp.status_code == 400
        assert notas_resp.body == "Peso a deve ser um número"
        
    
        