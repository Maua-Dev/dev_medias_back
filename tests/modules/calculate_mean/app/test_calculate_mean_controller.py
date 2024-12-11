import pytest
from src.modules.calculate_mean.app.calculate_mean_controller import CalculateMeanController

from src.modules.calculate_mean.app.calculate_mean_usecase import CalculateMeanUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest


class TestCalculateMeanController:

    def test_possible_grade_controller_1(self):
        request = HttpRequest(body={
            'provas_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.3
                }
            ],
            'trabalhos_que_tenho':[
                {
                    'valor':6.0,
                    'peso':0.3
                },
                {
                    'valor':6.0,
                    'peso':0.4
                },
            ],
        })

        usecase = CalculateMeanUsecase()
        controller = CalculateMeanController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 200
        assert response.body["message"] == "Média calculada com sucesso"
        assert response.body["media"] == 6.0
