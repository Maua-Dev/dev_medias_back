import pytest

from src.modules.grade_optimizer.app.grade_optmizer_usecase import GradeOptimizerUsecase
from src.shared.domain.entities.nota import Nota
from src.shared.helpers.errors.function_errors import FunctionInputError
from src.shared.helpers.errors.usecase_errors import InvalidInput
from src.shared.helpers.functions.utils import Utils
from src.shared.solucionador import Solucionador


class TestGradeOptimizerUsecase:

    def test_possible_grade_usecase(self):
        P1 = Nota(peso=0.12, valor=6.0)
        T1 = Nota(peso=0.08, valor=6.0)
        T2 = Nota(peso=0.08, valor=6.0)
        
        notas_que_tenho = [P1, T1, T2]

        P2 = Nota(peso=0.12, valor=None)
        P3 = Nota(peso=0.18, valor=None)
        T3 = Nota(peso=0.12, valor=None)
        P4 = Nota(peso=0.18, valor=None)
        T4 = Nota(peso=0.12, valor=None)
        
        notas_que_quero = [P2, P3, T3, P4, T4]
        
        media_desejada = 6.0

        usecase = GradeOptimizerUsecase()

        notas_resp = usecase(notas_que_tenho=notas_que_tenho, notas_que_quero=notas_que_quero, media_desejada=media_desejada)

        assert abs(round(Utils.media(notas_resp + notas_que_tenho) - media_desejada, 2)) <= Solucionador.ERR_MAX

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

            assert abs(round(Utils.media(notas_resp + notas_que_tenho) - media_desejada, 2)) <= Solucionador.ERR_MAX
            
    def test_possible_grade_usecase_3(self):
            P1 = Nota(peso=0.2*0.6, valor=5.0)
            notas_que_tenho = [P1]

            T1 = Nota(peso=0.08, valor=None)
            T2 = Nota(peso=0.08, valor=None)
            P2 = Nota(peso=0.2*0.6, valor=None)
            P3 = Nota(peso=0.3*0.6, valor=None)
            T3 = Nota(peso=0.3*0.4, valor=None)
            P4 = Nota(peso=0.3*0.6, valor=None)
            T4 = Nota(peso=0.3*0.4, valor=None)
            notas_que_quero = [T1, T2, P2, T3, P3, T4, P4]
            
            media_desejada = 6.0

            usecase = GradeOptimizerUsecase()

            notas_resp = usecase(notas_que_tenho=notas_que_tenho, notas_que_quero=notas_que_quero, media_desejada=media_desejada)

            assert abs(round(Utils.media(notas_resp + notas_que_tenho) - media_desejada, 2)) <= Solucionador.ERR_MAX
            
    def test_possible_grade_usecase_4(self):
            P1 = Nota(peso=0.2, valor=10.0)
            P2 = Nota(peso=0.2, valor=10.0)
            notas_que_tenho = [P1, P2]

            P3 = Nota(peso=0.4, valor = None)
            P4 = Nota(peso=0.2, valor = None)
            notas_que_quero = [P3, P4]
            
            media_desejada = 10

            usecase = GradeOptimizerUsecase()

            notas_resp = usecase(notas_que_tenho=notas_que_tenho, notas_que_quero=notas_que_quero, media_desejada=media_desejada)

            assert notas_resp[0].valor == 10.0
            
    def test_possible_grade_usecase_5(self):
            P1 = Nota(peso=0.2, valor=6.0)
            P2 = Nota(peso=0.2, valor=8.0)
            notas_que_tenho = [P1, P2]

            P3 = Nota(peso=0.3, valor=None)
            P4 = Nota(peso=0.3, valor=None)
            notas_que_quero = [P3, P4]
            
            media_desejada = 6

            usecase = GradeOptimizerUsecase()

            notas_resp = usecase(notas_que_tenho=notas_que_tenho, notas_que_quero=notas_que_quero, media_desejada=media_desejada)

            assert notas_resp[0].valor == 5.5
            assert notas_resp[1].valor == 5.5

    def test_possible_grade_usecase_nenhuma_nota_pedida(self):
        P1 = Nota(peso=0.12, valor=6.0)
        T1 = Nota(peso=0.08, valor=6.0)
        T2 = Nota(peso=0.08, valor=6.0)
        
        media_desejada = 6.0    
        
        usecase = GradeOptimizerUsecase()
        
        with pytest.raises(InvalidInput):
            usecase(notas_que_tenho=[P1, T1, T2], notas_que_quero=[], media_desejada=media_desejada)
            
    def test_possible_grade_usecase_impossivel_de_tirar_nota(self):
        P1 = Nota(peso=0.2, valor=0)
        P2 = Nota(peso=0.2, valor=8.0)
        notas_que_tenho = [P1, P2]
        
        P3 = Nota(peso=0.3)
        P4 = Nota(peso=0.3)
        notas_que_quero = [P3, P4]
        
        media_desejada = 10
        
        usecase = GradeOptimizerUsecase()
        
        notas_resp = usecase(notas_que_tenho=notas_que_tenho, notas_que_quero=notas_que_quero, media_desejada=media_desejada)
        
        assert notas_resp == []
        
    def test_possible_grade_usecase_impossivel_de_tirar_nota_2(self):
        P1 = Nota(peso=0.2*0.6, valor=6.0)
        T1 = Nota(peso=0.08, valor=6.0)
        T2 = Nota(peso=0.08, valor=6.0)
        notas_que_tenho = [P1, T1, T2]

        P2 = Nota(peso=0.2*0.6, valor=None)
        P3 = Nota(peso=0.3*0.6, valor=None)
        T3 = Nota(peso=0.3*0.4, valor=None)
        P4 = Nota(peso=0.3*0.6, valor=None)
        T4 = Nota(peso=0.3*0.4, valor=None)
        notas_que_quero = [P2, P3, T3, P4, T4]
        
        media_desejada = 10
        
        usecase = GradeOptimizerUsecase()
        
        notas_resp = usecase(notas_que_tenho=notas_que_tenho, notas_que_quero=notas_que_quero, media_desejada=media_desejada)
        
        assert notas_resp == []
        
    def test_possible_grade_usecase_uma_nota_apenas(self):
        P1 = Nota(peso=0.2, valor=6)
        P2 = Nota(peso=0.2, valor=8.0)
        P3 = Nota(peso=0.3, valor = 10.0)
        l_notas_que_tenho = [P1, P2, P3]
        
        P4 = Nota(peso=0.3, valor=None)
        l_notas_que_quero = [P4]

        media_desejada = 6
        
        notas_resp = GradeOptimizerUsecase()(notas_que_tenho=l_notas_que_tenho, notas_que_quero=l_notas_que_quero, media_desejada=media_desejada)
        
        assert notas_resp[0].valor == 1.0
        
    def test_possible_grade_usecase_uma_nota_apenas_2(self):
        P1 = Nota(peso=0.2, valor=10.0)
        P2 = Nota(peso=0.2, valor=10.0)
        P3 = Nota(peso=0.3, valor=10.0)
        notas_que_tenho = [P1, P2, P3]

        P4 = Nota(peso=0.3, valor=None)
        notas_que_quero = [P4]

        media_desejada = 6

        notas_resp = GradeOptimizerUsecase()(notas_que_tenho=notas_que_tenho, notas_que_quero=notas_que_quero, media_desejada=media_desejada)
        
        assert notas_resp[0].valor == 0.0
        
    def test_possible_grade_usecase_nao_pediu_nota(self):
        P1 = Nota(peso=0.12, valor=6.0)
        T1 = Nota(peso=0.08, valor=6.0)
        T2 = Nota(peso=0.08, valor=6.0)
        
        notas_que_tenho = [P1, T1, T2]

        notas_que_quero = []
        
        media_desejada = 6.0

        usecase = GradeOptimizerUsecase()


        with pytest.raises(InvalidInput):
            usecase(notas_que_tenho=notas_que_tenho, notas_que_quero=notas_que_quero, media_desejada=media_desejada)
            
    def test_possible_grade_usecase_media_desejada_menor_que_minimo_valor(self):
        P1 = Nota(peso=0.12, valor=6.0)
        T1 = Nota(peso=0.08, valor=6.0)
        T2 = Nota(peso=0.08, valor=6.0)
        
        notas_que_tenho = [P1, T1, T2]

        P2 = Nota(peso=0.12, valor=None)
        P3 = Nota(peso=0.18, valor=None)
        T3 = Nota(peso=0.12, valor=None)
        P4 = Nota(peso=0.18, valor=None)
        T4 = Nota(peso=0.12, valor=None)
        
        notas_que_quero = [P2, P3, T3, P4, T4]
        
        media_desejada = -1

        usecase = GradeOptimizerUsecase()

        with pytest.raises(InvalidInput):
            usecase(notas_que_tenho=notas_que_tenho, notas_que_quero=notas_que_quero, media_desejada=media_desejada)

    def test_possible_grade_usecase_media_desejada_maior_que_maximo_valor(self):
        P1 = Nota(peso=0.12, valor=6.0)
        T1 = Nota(peso=0.08, valor=6.0)
        T2 = Nota(peso=0.08, valor=6.0)
        
        notas_que_tenho = [P1, T1, T2]

        P2 = Nota(peso=0.12, valor=None)
        P3 = Nota(peso=0.18, valor=None)
        T3 = Nota(peso=0.12, valor=None)
        P4 = Nota(peso=0.18, valor=None)
        T4 = Nota(peso=0.12, valor=None)
        
        notas_que_quero = [P2, P3, T3, P4, T4]
        
        media_desejada = 10*10

        usecase = GradeOptimizerUsecase()

        with pytest.raises(InvalidInput):
            usecase(notas_que_tenho=notas_que_tenho, notas_que_quero=notas_que_quero, media_desejada=media_desejada)

    def test_possible_grade_usecase_soma_dos_pesos_nao_e_1(self):
        P1 = Nota(peso=0.12, valor=6.0)
        T1 = Nota(peso=0.08, valor=6.0)
        T2 = Nota(peso=0.08, valor=6.0)
        
        notas_que_tenho = [P1, T1, T2]

        P2 = Nota(peso=0.12, valor=None)
        P3 = Nota(peso=0.2, valor=None)
        T3 = Nota(peso=0.12, valor=None)
        P4 = Nota(peso=0.18, valor=None)
        T4 = Nota(peso=0.12, valor=None)
        
        notas_que_quero = [P2, P3, T3, P4, T4]
        
        media_desejada = 6.0

        usecase = GradeOptimizerUsecase()

        with pytest.raises(FunctionInputError):
            usecase(notas_que_tenho=notas_que_tenho, notas_que_quero=notas_que_quero, media_desejada=media_desejada)
            