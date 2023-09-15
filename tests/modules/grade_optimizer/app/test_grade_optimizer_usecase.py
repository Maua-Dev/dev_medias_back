import pytest

from src.modules.grade_optmizer.app.grade_optmizer_usecase import GradeOptimizerUsecase
from src.shared.domain.entities.nota import Nota
from src.shared.helpers.errors.domain_errors import EntityParameterError
from src.shared.helpers.errors.function_errors import FunctionInputError
from src.shared.helpers.errors.usecase_errors import CombinationNotFound, InvalidInput
from src.shared.helpers.functions.utils import Utils
from src.shared.solucionador import Solucionador


class TestGradeOptimizerUsecase:

    def test_possible_grade_usecase(self):
        P1 = Nota(peso=0.12, valor=6.0)
        T1 = Nota(peso=0.08, valor=6.0)
        T2 = Nota(peso=0.08, valor=6.0)
        
        provas_que_tenho = [P1]
        trabalhos_que_tenho = [T1, T2]

        P2 = Nota(peso=0.12, valor=None)
        P3 = Nota(peso=0.18, valor=None)
        T3 = Nota(peso=0.12, valor=None)
        P4 = Nota(peso=0.18, valor=None)
        T4 = Nota(peso=0.12, valor=None)
        
        provas_que_quero = [P2, P3, P4]
        trabalhos_que_quero = [T3, T4]
        
        media_desejada = 6.0

        usecase = GradeOptimizerUsecase()

        for _ in range(10):
            boletim_resp = usecase(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho, media_desejada=media_desejada)
            assert abs(round(boletim_resp.media_final() - media_desejada, 2)) <= Solucionador.ERR_MAX

    def test_possible_grade_usecase_2(self):
        P1 = Nota(peso=0.2, valor=6.0)
        P2 = Nota(peso=0.2, valor=8.0)
        provas_que_tenho = [P1, P2]
        trabalhos_que_tenho = []
        
        P3 = Nota(peso=0.3, valor=None)
        P4 = Nota(peso=0.3, valor=None)
        provas_que_quero = [P3, P4]
        trabalhos_que_quero = []
        
        media_desejada = 7.0 

        usecase = GradeOptimizerUsecase()

        for _ in range(10):
            boletim_resp = usecase(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho, media_desejada=media_desejada)

            assert abs(round(boletim_resp.media_final() - media_desejada, 2)) <= Solucionador.ERR_MAX
            
    def test_possible_grade_usecase_3(self):
        P1 = Nota(peso=0.2*0.6, valor=5.0)
        provas_que_tenho = [P1]
        trabalhos_que_tenho = []

        T1 = Nota(peso=0.08, valor=None)
        T2 = Nota(peso=0.08, valor=None)
        P2 = Nota(peso=0.2*0.6, valor=None)
        P3 = Nota(peso=0.3*0.6, valor=None)
        T3 = Nota(peso=0.3*0.4, valor=None)
        P4 = Nota(peso=0.3*0.6, valor=None)
        T4 = Nota(peso=0.3*0.4, valor=None)
        provas_que_quero = [P2, P3, P4]
        trabalhos_que_quero = [T1, T2, T3, T4]
    
        media_desejada = 6.0

        usecase = GradeOptimizerUsecase()

        for _ in range(10):
            boletim_resp = usecase(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho, media_desejada=media_desejada)

            assert abs(round(boletim_resp.media_final() - media_desejada, 2)) <= Solucionador.ERR_MAX
            
    def test_possible_grade_usecase_4(self):
        P1 = Nota(peso=0.2, valor=10.0)
        P2 = Nota(peso=0.2, valor=10.0)
        provas_que_tenho = [P1, P2]
        trabalhos_que_tenho = []

        P3 = Nota(peso=0.4, valor = None)
        P4 = Nota(peso=0.2, valor = None)
        provas_que_quero = [P3, P4]
        trabalhos_que_quero = []
        
        media_desejada = 10

        usecase = GradeOptimizerUsecase()

        for _ in range(10):
            boletim_resp = usecase(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho, media_desejada=media_desejada)

            assert boletim_resp.quero[0].valor == 10.0
            assert boletim_resp.quero[1].valor == 10.0
                  
    def test_possible_grade_usecase_5(self):
        P1 = Nota(peso=0.2, valor=6.0)
        P2 = Nota(peso=0.2, valor=8.0)
        provas_que_tenho = [P1, P2]
        trabalhos_que_tenho = []

        P3 = Nota(peso=0.3, valor=None)
        P4 = Nota(peso=0.3, valor=None)
        provas_que_quero = [P3, P4]
        trabalhos_que_quero = []
        
        media_desejada = 6

        usecase = GradeOptimizerUsecase()

        for _ in range(10):
            boletim_resp = usecase(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho, media_desejada=media_desejada)

            assert boletim_resp.quero[0].valor == 5.0 and boletim_resp.quero[1].valor == 5.5 or boletim_resp.quero[0].valor == 5.5 and boletim_resp.quero[1].valor == 5.0
            assert abs(round(boletim_resp.media_final() - media_desejada, 2)) <= Solucionador.ERR_MAX
            
    def test_possible_grade_usecase_6(self):
        P1 = Nota(peso=0.2, valor=1.0)
        provas_que_tenho = [P1]
        trabalhos_que_tenho = []

        P2 = Nota(peso=0.2, valor=None)
        provas_que_quero = [P2]
        
        T1 = Nota(peso=0.3, valor=None)
        T2 = Nota(peso=0.3, valor=None)
        trabalhos_que_quero = [T1, T2]
        
        media_desejada = 6

        usecase = GradeOptimizerUsecase()

        for _ in range(10):
            boletim_resp = usecase(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho, media_desejada=media_desejada)

            assert abs(round(boletim_resp.media_final() - media_desejada, 2)) <= Solucionador.ERR_MAX
    
    def test_possible_grade_usecase_7(self):
        P1 = Nota(peso=0.15, valor=6.0)
        provas_que_tenho = [P1]
        trabalhos_que_tenho = []

        P2 = Nota(peso=0.15, valor=5.0)
        P3 = Nota(peso=0.15, valor=None)
        P4 = Nota(peso=0.15, valor=None)
        provas_que_quero = [P2, P3, P4]
        
        T1 = Nota(peso=0.1, valor=None)
        T2 = Nota(peso=0.1, valor=None)
        T3 = Nota(peso=0.1, valor=None)
        T4 = Nota(peso=0.1, valor=None)
        trabalhos_que_quero = [T1, T2, T3, T4]
        
        media_desejada = 6

        usecase = GradeOptimizerUsecase()

        for _ in range(10):
            boletim_resp = usecase(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho, media_desejada=media_desejada)
            assert abs(round(boletim_resp.media_final() - media_desejada, 2)) <= Solucionador.ERR_MAX
    
    def test_possible_grade_usecase_8(self):
        provas_que_tenho = []
        
        T1 = Nota(peso=0.234375, valor=7.5)
        T2 = Nota(peso=0.234375, valor=8.5)
        trabalhos_que_tenho = [T1, T2]

        provas_que_quero = []
        
        T3 = Nota(peso=0.234375, valor=None)
        T4 = Nota(peso=0.234375, valor=None)
        T5 = Nota(peso=0.0625, valor=None)
        trabalhos_que_quero = [T3, T4, T5]
        
        media_desejada = 6

        usecase = GradeOptimizerUsecase()

        for _ in range(10):
            boletim_resp = usecase(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho, media_desejada=media_desejada)
            assert abs(round(boletim_resp.media_final() - media_desejada, 2)) <= Solucionador.ERR_MAX

    def test_possible_grade_usecase_nenhuma_nota_pedida(self):
        P1 = Nota(peso=0.12, valor=6.0)
        provas_que_tenho = [P1]
        T1 = Nota(peso=0.08, valor=6.0)
        T2 = Nota(peso=0.08, valor=6.0)
        trabalhos_que_tenho = [T1, T2]
        provas_que_quero = []
        trabalhos_que_quero = []

        
        media_desejada = 6.0    
        
        usecase = GradeOptimizerUsecase()
        
        with pytest.raises(InvalidInput):
            usecase(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho, media_desejada=media_desejada)
            
    def test_possible_grade_usecase_impossivel_de_tirar_nota(self):
        P1 = Nota(peso=0.2, valor=0)
        P2 = Nota(peso=0.2, valor=8.0)
        provas_que_tenho = [P1, P2]
        trabalhos_que_tenho = []
        
        P3 = Nota(peso=0.3)
        P4 = Nota(peso=0.3)
        provas_que_quero = [P3, P4]
        trabalhos_que_quero = []
        
        media_desejada = 10
        
        usecase = GradeOptimizerUsecase()
        
        for _ in range(10):
            with pytest.raises(CombinationNotFound):
                usecase(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho, media_desejada=media_desejada)
 
    def test_possible_grade_usecase_impossivel_de_tirar_nota_2(self):
        P1 = Nota(peso=0.2*0.6, valor=6.0)
        T1 = Nota(peso=0.08, valor=6.0)
        T2 = Nota(peso=0.08, valor=6.0)
        provas_que_tenho = [P1]
        trabalhos_que_tenho = [T1, T2]

        P2 = Nota(peso=0.2*0.6, valor=None)
        P3 = Nota(peso=0.3*0.6, valor=None)
        T3 = Nota(peso=0.3*0.4, valor=None)
        P4 = Nota(peso=0.3*0.6, valor=None)
        T4 = Nota(peso=0.3*0.4, valor=None)
        provas_que_quero = [P2, P3, P4]
        trabalhos_que_quero = [T3, T4]
        
        media_desejada = 10
        
        usecase = GradeOptimizerUsecase()
        
        for _ in range(10):
            with pytest.raises(CombinationNotFound):
                usecase(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho, media_desejada=media_desejada)

    def test_possible_grade_usecase_uma_nota_apenas(self):
        P1 = Nota(peso=0.2, valor=6)
        P2 = Nota(peso=0.2, valor=8.0)
        T1 = Nota(peso=0.3, valor = 10.0)
        provas_que_tenho = [P1, P2]
        trabalhos_que_tenho = [T1]
        
        
        T2 = Nota(peso=0.3, valor=None)
        trabalhos_que_quero = [T2]
        provas_que_quero = []

        media_desejada = 6
        
        usecase = GradeOptimizerUsecase()
        
        for _ in range(10):
            boletim_resp = usecase(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho, media_desejada=media_desejada)

            assert boletim_resp.quero[0].valor == 1.0
        
    def test_possible_grade_usecase_uma_nota_apenas_2(self):
        P1 = Nota(peso=0.2, valor=10.0)
        T1 = Nota(peso=0.2, valor=10.0)
        T2 = Nota(peso=0.3, valor=10.0)
        provas_que_tenho = [P1]
        trabalhos_que_tenho = [T1, T2]

        P2 = Nota(peso=0.3, valor=None)
        provas_que_quero = [P2]
        trabalhos_que_quero = []

        media_desejada = 6
        
        usecase = GradeOptimizerUsecase()

        for _ in range(10):
            boletim_resp = usecase(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho, media_desejada=media_desejada)

            assert boletim_resp.quero[0].valor == 0.0
        
    def test_possible_grade_usecase_nao_pediu_nota(self):
        P1 = Nota(peso=0.12, valor=6.0)
        T1 = Nota(peso=0.08, valor=6.0)
        T2 = Nota(peso=0.08, valor=6.0)
        provas_que_tenho = [P1]
        trabalhos_que_tenho = [T1, T2]
        provas_que_quero = []
        trabalhos_que_quero = []
        
        media_desejada = 6.0

        usecase = GradeOptimizerUsecase()


        with pytest.raises(InvalidInput):
            usecase(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho, media_desejada=media_desejada)
            
    def test_possible_grade_usecase_media_desejada_menor_que_minimo_valor(self):
        P1 = Nota(peso=0.12, valor=6.0)
        T1 = Nota(peso=0.08, valor=6.0)
        T2 = Nota(peso=0.08, valor=6.0)
        provas_que_tenho = [P1]
        trabalhos_que_tenho = [T1, T2]

        P2 = Nota(peso=0.12, valor=None)
        P3 = Nota(peso=0.18, valor=None)
        T3 = Nota(peso=0.12, valor=None)
        P4 = Nota(peso=0.18, valor=None)
        T4 = Nota(peso=0.12, valor=None)
        provas_que_quero = [P2, P3, P4]
        trabalhos_que_quero = [T3, T4]
        
        media_desejada = -1

        usecase = GradeOptimizerUsecase()

        with pytest.raises(InvalidInput):
            usecase(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho, media_desejada=media_desejada)

    def test_possible_grade_usecase_media_desejada_maior_que_maximo_valor(self):
        P1 = Nota(peso=0.12, valor=6.0)
        T1 = Nota(peso=0.08, valor=6.0)
        T2 = Nota(peso=0.08, valor=6.0)
        provas_que_tenho = [P1]
        trabalhos_que_tenho = [T1, T2]

        P2 = Nota(peso=0.12, valor=None)
        P3 = Nota(peso=0.18, valor=None)
        T3 = Nota(peso=0.12, valor=None)
        P4 = Nota(peso=0.18, valor=None)
        T4 = Nota(peso=0.12, valor=None)
        provas_que_quero = [P2, P3, P4]
        trabalhos_que_quero = [T3, T4]
        
        media_desejada = 10*10

        usecase = GradeOptimizerUsecase()

        with pytest.raises(InvalidInput):
            usecase(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho, media_desejada=media_desejada)

    def test_possible_grade_usecase_soma_dos_pesos_nao_e_1(self):
        P1 = Nota(peso=0.12, valor=6.0)
        T1 = Nota(peso=0.08, valor=6.0)
        T2 = Nota(peso=0.08, valor=6.0)
        provas_que_tenho = [P1]
        trabalhos_que_tenho = [T1, T2]

        P2 = Nota(peso=0.12, valor=None)
        P3 = Nota(peso=0.2, valor=None)
        T3 = Nota(peso=0.12, valor=None)
        P4 = Nota(peso=0.18, valor=None)
        T4 = Nota(peso=0.12, valor=None)
        provas_que_quero = [P2, P3, P4]
        trabalhos_que_quero = [T3, T4]
        
        media_desejada = 6.0

        usecase = GradeOptimizerUsecase()

        with pytest.raises(EntityParameterError):
            usecase(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho, media_desejada=media_desejada)
            