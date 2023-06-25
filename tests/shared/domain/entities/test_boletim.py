import pytest
from src.shared.domain.entities.boletim import Boletim
from src.shared.domain.entities.conjunto_de_notas import ConjuntoDeNotas
from src.shared.domain.entities.nota import Nota
from src.shared.helpers.errors.domain_errors import EntityParameterError
from src.shared.helpers.errors.function_errors import FunctionInputError


class Test_Boletim:
    def test_boletim(self):
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
        
        provas = ConjuntoDeNotas(quero=provas_que_quero, tenho=provas_que_tenho)
        trabalhos = ConjuntoDeNotas(quero=trabalhos_que_quero, tenho=trabalhos_que_tenho)
        boletim = Boletim(provas=provas, trabalhos=trabalhos)
        
        assert str(boletim.provas) == str(provas)
        assert str(boletim.trabalhos) == str(trabalhos)
        assert str(boletim.provas.tenho) == str(provas_que_tenho)
        assert str(boletim.trabalhos.tenho) == str(trabalhos_que_tenho)
        assert str(boletim.provas.quero) == str(provas_que_quero)
        assert str(boletim.trabalhos.quero) == str(trabalhos_que_quero)        
        
    def test_boletim_pesos_nao_dao_1(self):
        P1 = Nota(peso=0.12, valor=6.0)
        T1 = Nota(peso=0.08, valor=6.0)
        T2 = Nota(peso=0.08, valor=6.0)
        
        provas_que_tenho = [P1]
        trabalhos_que_tenho = [T1, T2]

        P2 = Nota(peso=0.12, valor=None)
        P3 = Nota(peso=0.19, valor=None)
        T3 = Nota(peso=0.12, valor=None)
        P4 = Nota(peso=0.18, valor=None)
        T4 = Nota(peso=0.12, valor=None)
        
        provas_que_quero = [P2, P3, P4]
        trabalhos_que_quero = [T3, T4]
        
        provas = ConjuntoDeNotas(quero=provas_que_quero, tenho=provas_que_tenho)
        trabalhos = ConjuntoDeNotas(quero=trabalhos_que_quero, tenho=trabalhos_que_tenho)
        with pytest.raises(FunctionInputError):
            Boletim(provas=provas, trabalhos=trabalhos)
        
    def test_boletim_provas_nao_sao_conjunto_de_notas(self):
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
        
        provas = provas_que_quero
        trabalhos = ConjuntoDeNotas(quero=trabalhos_que_quero, tenho=trabalhos_que_tenho)
        
        with pytest.raises(EntityParameterError):
            Boletim(provas=provas, trabalhos=trabalhos)   
            
    def test_boletim_trabalhos_nao_sao_conjunto_de_notas(self):
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
        
        provas = ConjuntoDeNotas(quero=provas_que_quero, tenho=provas_que_tenho)
        trabalhos = trabalhos_que_quero
        
        with pytest.raises(EntityParameterError):
            Boletim(provas=provas, trabalhos=trabalhos)   
            
    def test_boletim_media_final(self):
        P1 = Nota(peso=0.24, valor=1)
        P2 = Nota(peso=0.36, valor=None)
        T1 = Nota(peso=0.12, valor=None)
        T2 = Nota(peso=0.28, valor=None)
        
        provas = ConjuntoDeNotas(quero=[P2], tenho=[P1])
        trabalhos = ConjuntoDeNotas(quero=[T1, T2], tenho=[])
        boletim = Boletim(provas=provas, trabalhos=trabalhos)
        
        boletim.provas.quero[0].valor = 7.5
        boletim.trabalhos.quero[0].valor = 7.5
        boletim.trabalhos.quero[1].valor = 8

        assert boletim.media_final() == 6.0      