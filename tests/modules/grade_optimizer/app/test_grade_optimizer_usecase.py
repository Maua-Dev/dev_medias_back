import pytest

from src.modules.grade_optimizer.app.grade_optmizer_usecase import GradeOptimizerUsecase
from src.shared.domain.entities.nota import Nota
from src.shared.helpers.errors.usecase_errors import InvalidInput
from src.shared.helpers.functions.utils import Utils
from src.shared.solucionador import Solucionador


class TestGradeOptimizerUsecase:

    def test_possible_grade_usecase(self):
        P1 = Nota(peso=0.12, valor=6.0)
        T1 = Nota(peso=0.08, valor=6.0)
        T2 = Nota(peso=0.08, valor=6.0)
        P2 = Nota(peso=0.12, valor=None)
        P3 = Nota(peso=0.18, valor=None)
        T3 = Nota(peso=0.12, valor=None)
        P4 = Nota(peso=0.18, valor=None)
        T4 = Nota(peso=0.12, valor=None)
        media_desejada = 6.0

        usecase = GradeOptimizerUsecase()

        notas_resp = usecase(notas_que_tenho=[P1, T1, T2], notas_que_quero=[P2, P3, T3, P4, T4], media_desejada=media_desejada)

        assert abs(Utils.media(notas_resp + [P1, T1, T2]) - media_desejada) <= Solucionador.ERR_MAX

    def test_possible_grade_usecase_2(self):
            P1 = Nota(peso=0.2, valor=6.0)
            P2 = Nota(peso=0.2, valor=8.0)
            notas_que_tenho = [P1, P2]
            
            P3 = Nota(peso=0.3, valor=None)
            P4 = Nota(peso=0.3, valor=None)
            notas_que_quero = [P3, P4]
            
            media_desejada = 7.0 #6.0

            usecase = GradeOptimizerUsecase()

            notas_resp = usecase(notas_que_tenho=notas_que_tenho, notas_que_quero=notas_que_quero, media_desejada=media_desejada)

            assert abs(Utils.media(notas_resp + notas_que_tenho) - media_desejada) <= Solucionador.ERR_MAX

    def test_possible_grade_usecase_nenhuma_nota_pedida(self):
        P1 = Nota(peso=0.12, valor=6.0)
        T1 = Nota(peso=0.08, valor=6.0)
        T2 = Nota(peso=0.08, valor=6.0)
        
        media_desejada = 6.0    
        
        usecase = GradeOptimizerUsecase()
        
        with pytest.raises(InvalidInput):
            usecase(notas_que_tenho=[P1, T1, T2], notas_que_quero=[], media_desejada=media_desejada)