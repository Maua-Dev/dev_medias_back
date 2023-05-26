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
        assert notas_resp.body["message"] == "the algorithm retrieved a possible combination of grades successfully"
