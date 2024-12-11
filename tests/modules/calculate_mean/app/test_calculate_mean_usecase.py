import pytest

from src.modules.calculate_mean.app.calculate_mean_usecase import CalculateMeanUsecase
from src.shared.domain.entities.nota import Nota
from src.shared.helpers.errors.domain_errors import EntityParameterError
from src.shared.helpers.errors.function_errors import FunctionInputError
from src.shared.helpers.errors.usecase_errors import CombinationNotFound, InvalidInput
from src.shared.helpers.functions.utils import Utils
from src.shared.solucionador import Solucionador


class TestCalculateMeanUsecase:

    def test_calculate_mean_usecase(self):
        P1 = Nota(peso=0.6*0.4, valor=5)
        P2 = Nota(peso=0.6*0.6, valor=4)
        provas_que_tenho = [P1, P2]
        
        T1 = Nota(peso=0.4*0.4, valor=9.5)
        T2 = Nota(peso=0.4*0.6, valor=7)
        trabalhos_que_tenho = [T1, T2]
        
        

        usecase = CalculateMeanUsecase()
        mean = usecase(provas_que_tenho=provas_que_tenho, trabalhos_que_tenho=trabalhos_que_tenho)

        assert mean == 5.8

    def test_calculate_mean_empty_list(self):
        provas_que_tenho = []
        trabalhos_que_tenho = []
        usecase = CalculateMeanUsecase()

        with pytest.raises(InvalidInput):
            usecase(provas_que_tenho=provas_que_tenho, trabalhos_que_tenho=trabalhos_que_tenho)
            
    def test_calculate_mean_prova_without_value(self):
        P1 = Nota(peso=0.6*0.4)
        P2 = Nota(peso=0.6*0.6, valor=4)
        provas_que_tenho = [P1, P2]
        
        T1 = Nota(peso=0.4*0.4, valor=9.5)
        T2 = Nota(peso=0.4*0.6, valor=7)
        trabalhos_que_tenho = [T1, T2]
        usecase = CalculateMeanUsecase()

        with pytest.raises(FunctionInputError):
            usecase(provas_que_tenho=provas_que_tenho, trabalhos_que_tenho=trabalhos_que_tenho)
            
    def test_calculate_mean_trabalho_without_value(self):
        P1 = Nota(peso=0.6*0.4, valor=4)
        P2 = Nota(peso=0.6*0.6, valor=4)
        provas_que_tenho = [P1, P2]
        
        T1 = Nota(peso=0.4*0.4, valor=9.5)
        T2 = Nota(peso=0.4*0.6)
        trabalhos_que_tenho = [T1, T2]
        usecase = CalculateMeanUsecase()

        with pytest.raises(FunctionInputError):
            usecase(provas_que_tenho=provas_que_tenho, trabalhos_que_tenho=trabalhos_que_tenho)
    