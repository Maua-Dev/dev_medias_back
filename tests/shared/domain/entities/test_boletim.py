import pytest
from src.shared.domain.entities.boletim import Boletim
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
        
        boletim = Boletim(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho)
        
        notas_que_tenho = provas_que_tenho + trabalhos_que_tenho
        notas_que_quero = provas_que_quero + trabalhos_que_quero
        
        assert all([boletim.tenho[i] == notas_que_tenho[i] for i in range(len(notas_que_tenho))])
        assert all([boletim.quero[i] == notas_que_quero[i] for i in range(len(notas_que_quero))])
        assert boletim.idx_quero == len(provas_que_quero)
        assert boletim.idx_tenho == len(provas_que_tenho)
        
    def test_boletim_sem_trabalhos(self):
        P1 = Nota(peso=0.2, valor=6.0)
        
        provas_que_tenho = [P1]
        trabalhos_que_tenho = []

        P2 = Nota(peso=0.2, valor=None)
        P3 = Nota(peso=0.3, valor=None)
        P4 = Nota(peso=0.3, valor=None)
        
        provas_que_quero = [P2, P3, P4]
        trabalhos_que_quero = []
        
        boletim = Boletim(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho)
        
        notas_que_tenho = provas_que_tenho + trabalhos_que_tenho
        notas_que_quero = provas_que_quero + trabalhos_que_quero
        
        assert all([boletim.tenho[i] == notas_que_tenho[i] for i in range(len(notas_que_tenho))])
        assert all([boletim.quero[i] == notas_que_quero[i] for i in range(len(notas_que_quero))])
        assert boletim.idx_quero == len(provas_que_quero)
        assert boletim.idx_tenho == len(provas_que_tenho)
        
    def test_boletim_sem_provas(self):
        T1 = Nota(peso=0.2, valor=6.0)
        T2 = Nota(peso=0.2, valor=6.0)
        
        provas_que_tenho = []
        trabalhos_que_tenho = [T1, T2]

        T3 = Nota(peso=0.3, valor=None)
        T4 = Nota(peso=0.3, valor=None)
        
        provas_que_quero = []
        trabalhos_que_quero = [T3, T4]
        
        boletim = Boletim(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho)
        
        notas_que_tenho = provas_que_tenho + trabalhos_que_tenho
        notas_que_quero = provas_que_quero + trabalhos_que_quero
        
        assert all([boletim.tenho[i] == notas_que_tenho[i] for i in range(len(notas_que_tenho))])
        assert all([boletim.quero[i] == notas_que_quero[i] for i in range(len(notas_que_quero))])
        assert boletim.idx_quero == len(provas_que_quero)
        assert boletim.idx_tenho == len(provas_que_tenho)
        
    def test_boletim_provas_que_tenho_nao_lista_de_notas(self):
        P1 = Nota(peso=0.12, valor=6.0)
        T1 = Nota(peso=0.08, valor=6.0)
        T2 = Nota(peso=0.08, valor=6.0)
        
        provas_que_tenho = P1
        trabalhos_que_tenho = [T1, T2]

        P2 = Nota(peso=0.12, valor=None)
        P3 = Nota(peso=0.18, valor=None)
        T3 = Nota(peso=0.12, valor=None)
        P4 = Nota(peso=0.18, valor=None)
        T4 = Nota(peso=0.12, valor=None)
        
        provas_que_quero = [P2, P3, P4]
        trabalhos_que_quero = [T3, T4]
        
        with pytest.raises(EntityParameterError):
            Boletim(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho)
            
    def test_boletim_provas_que_quero_nao_lista_de_notas(self):
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
        
        provas_que_quero = P2
        trabalhos_que_quero = [T3, T4]
        
        with pytest.raises(EntityParameterError):
            Boletim(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho)
            
    def test_boletim_trabalhos_que_tenho_nao_lista_de_notas(self):
        P1 = Nota(peso=0.12, valor=6.0)
        T1 = Nota(peso=0.08, valor=6.0)
        T2 = Nota(peso=0.08, valor=6.0)
        
        provas_que_tenho = [P1]
        trabalhos_que_tenho = T1

        P2 = Nota(peso=0.12, valor=None)
        P3 = Nota(peso=0.18, valor=None)
        T3 = Nota(peso=0.12, valor=None)
        P4 = Nota(peso=0.18, valor=None)
        T4 = Nota(peso=0.12, valor=None)
        
        provas_que_quero = [P2, P3, P4]
        trabalhos_que_quero = [T3, T4]
        
        with pytest.raises(EntityParameterError):
            Boletim(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho)
            
    def test_boletim_trabalhos_que_quero_nao_lista_de_notas(self):
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
        trabalhos_que_quero = T3
        
        with pytest.raises(EntityParameterError):
            Boletim(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho)
            
    def test_boletim_pesos_invalidos(self):
        P1 = Nota(peso=0.12, valor=6.0)
        T1 = Nota(peso=0.08, valor=6.0)
        T2 = Nota(peso=0.08, valor=6.0)
        
        provas_que_tenho = [P1]
        trabalhos_que_tenho = [T1, T2]

        P2 = Nota(peso=0.12, valor=None)
        P3 = Nota(peso=0.18, valor=None)
        T3 = Nota(peso=0.12, valor=None)
        P4 = Nota(peso=0.18, valor=None)
        T4 = Nota(peso=0.13, valor=None)
        
        provas_que_quero = [P2, P3, P4]
        trabalhos_que_quero = [T3, T4]
        
        with pytest.raises(EntityParameterError):
            Boletim(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho)
    
    def test_media_final_floor(self):
        P1 = Nota(peso=0.24, valor=1.0)
        provas_que_tenho = [P1]
        
        trabalhos_que_tenho = []
        
        P2 = Nota(peso=0.36, valor=None)
        provas_que_quero = [P2]
        
        T1 = Nota(peso=0.12, valor=None)
        T2 = Nota(peso=0.28, valor=None)
        trabalhos_que_quero = [T1, T2]
        
        boletim = Boletim(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho)
        
        boletim.quero[0].valor = 7.5
        boletim.quero[1].valor = 7.5
        boletim.quero[2].valor = 8
        
        assert boletim.media_final() == 6.0
        
    def test_media_final_floor(self):
        
        
        P1 = Nota(peso=0.2*0.5, valor=8)
        P2 = Nota(peso=0.2*0.5, valor=8)
        P3 = Nota(peso=0.3*0.5, valor=10)
        P4 = Nota(peso=0.3*0.5, valor=10)
        provas_que_tenho = [P1, P2, P3, P4]
        provas_que_quero = []
        
        T1 = Nota(peso=0.5*0.5, valor=10)
        T2 = Nota(peso=0.5*0.5, valor=10)
        trabalhos_que_tenho = [T1, T2]
        trabalhos_que_quero = []
        
        boletim = Boletim(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho)
        
        
        assert boletim.media_final() == 9.6
        
    def test_media_final_ceil(self):
        P1 = Nota(peso=0.24, valor=4)
        provas_que_tenho = [P1]
        
        trabalhos_que_tenho = []
        
        P2 = Nota(peso=0.36, valor=None)
        provas_que_quero = [P2]
        
        T1 = Nota(peso=0.12, valor=None)
        T2 = Nota(peso=0.28, valor=None)
        trabalhos_que_quero = [T1, T2]
        
        boletim = Boletim(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho)
        
        boletim.quero[0].valor = 7.5
        boletim.quero[1].valor = 7.5
        boletim.quero[2].valor = 8
        
        assert boletim.media_final() == 6.8
        
    def test_provas(self):
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
        
        provas = [P1, P2, P3, P4]
        trabalhos = [T1, T2, T3, T4]
        
        boletim = Boletim(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho)
        
        assert all([boletim.provas()[i] == provas[i] for i in range(len(provas))])
        
    def test_provas_sem_trabalhos(self):
        P1 = Nota(peso=0.2, valor=6.0)
        
        provas_que_tenho = [P1]
        trabalhos_que_tenho = []

        P2 = Nota(peso=0.2, valor=None)
        P3 = Nota(peso=0.3, valor=None)
        P4 = Nota(peso=0.3, valor=None)
        
        provas_que_quero = [P2, P3, P4]
        trabalhos_que_quero = []
        
        provas = [P1, P2, P3, P4]
        trabalhos = []
        
        boletim = Boletim(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho)
        
        assert all([boletim.provas()[i] == provas[i] for i in range(len(provas))])
        
    def test_provas_sem_provas(self):
        T1 = Nota(peso=0.2, valor=6.0)
        
        provas_que_tenho = []
        trabalhos_que_tenho = [T1]

        T2 = Nota(peso=0.2, valor=None)
        T3 = Nota(peso=0.3, valor=None)
        T4 = Nota(peso=0.3, valor=None)
        
        provas_que_quero = []
        trabalhos_que_quero = [T2, T3, T4]
        
        provas = []
        trabalhos = [T1, T2, T3, T4]
        
        boletim = Boletim(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho)
        
        assert all([boletim.provas()[i] == provas[i] for i in range(len(provas))])
        
    def test_trabalhos(self):
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
        
        provas = [P1, P2, P3, P4]
        trabalhos = [T1, T2, T3, T4]
        
        boletim = Boletim(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho)
        
        assert all([boletim.trabalhos()[i] == trabalhos[i] for i in range(len(trabalhos))])
        
    def test_trabalhos_sem_trabalhos(self):
        P1 = Nota(peso=0.2, valor=6.0)
        
        provas_que_tenho = [P1]
        trabalhos_que_tenho = []

        P2 = Nota(peso=0.2, valor=None)
        P3 = Nota(peso=0.3, valor=None)
        P4 = Nota(peso=0.3, valor=None)
        
        provas_que_quero = [P2, P3, P4]
        trabalhos_que_quero = []
        
        provas = [P1, P2, P3, P4]
        trabalhos = []
        
        boletim = Boletim(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho)
        
        assert all([boletim.trabalhos()[i] == trabalhos[i] for i in range(len(trabalhos))])
        
    def test_trabalhos_sem_provas(self):
        T1 = Nota(peso=0.2, valor=6.0)
        
        provas_que_tenho = []
        trabalhos_que_tenho = [T1]

        T2 = Nota(peso=0.2, valor=None)
        T3 = Nota(peso=0.3, valor=None)
        T4 = Nota(peso=0.3, valor=None)
        
        provas_que_quero = []
        trabalhos_que_quero = [T2, T3, T4]
        
        provas = []
        trabalhos = [T1, T2, T3, T4]
        
        boletim = Boletim(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho)
        
        assert all([boletim.trabalhos()[i] == trabalhos[i] for i in range(len(trabalhos))])
        
    def test_media_provas(self):
        P1 = Nota(peso=0.24, valor=1.0)
        provas_que_tenho = [P1]
        
        trabalhos_que_tenho = []
        
        P2 = Nota(peso=0.36, valor=None)
        provas_que_quero = [P2]
        
        T1 = Nota(peso=0.12, valor=None)
        T2 = Nota(peso=0.28, valor=None)
        trabalhos_que_quero = [T1, T2]
        
        boletim = Boletim(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho)
        
        boletim.quero[0].valor = 7.5
        boletim.quero[1].valor = 7.5
        boletim.quero[2].valor = 8
        
        assert boletim.media_provas() == 2.9
        
    def test_media_trabalhos(self):
        P1 = Nota(peso=0.24, valor=1.0)
        provas_que_tenho = [P1]
        
        trabalhos_que_tenho = []
        
        P2 = Nota(peso=0.36, valor=None)
        provas_que_quero = [P2]
        
        T1 = Nota(peso=0.12, valor=None)
        T2 = Nota(peso=0.28, valor=None)
        trabalhos_que_quero = [T1, T2]
        
        boletim = Boletim(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho)
        
        boletim.quero[0].valor = 7.5
        boletim.quero[1].valor = 7.5
        boletim.quero[2].valor = 8
        
        assert boletim.media_trabalhos() == 3.1
        
    def test_media_provas_devem_estar_preenchidas(self):
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
        
        boletim = Boletim(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho)
        
        with pytest.raises(FunctionInputError):
            boletim.media_provas()
            
    def test_media_trabalhos_devem_estar_preenchidos(self):
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
        
        boletim = Boletim(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho)
        
        with pytest.raises(FunctionInputError):
            boletim.media_trabalhos()
    
    def test_media_final_externo(self):
        P1 = Nota(peso=0.24, valor=1.0)
        provas_que_tenho = [P1]
        
        trabalhos_que_tenho = []
        
        P2 = Nota(peso=0.36, valor=7.5)
        provas_que_quero = [P2]
        
        T1 = Nota(peso=0.12, valor=7.5)
        T2 = Nota(peso=0.28, valor=8)
        trabalhos_que_quero = [T1, T2]
        
        tenho = provas_que_tenho + trabalhos_que_tenho
        quero = provas_que_quero + trabalhos_que_quero
        idx_tenho = len(provas_que_tenho)
        idx_quero = len(provas_que_quero)
        
        assert Boletim.media_final_externo(idx_tenho=idx_tenho, idx_quero=idx_quero, tenho=tenho, quero=quero) == 6.0
        
    def test_provas_que_quero(self):
        P1 = Nota(peso=0.24, valor=1.0)
        provas_que_tenho = [P1]
        
        trabalhos_que_tenho = []
        
        P2 = Nota(peso=0.36, valor=None)
        provas_que_quero = [P2]
        
        T1 = Nota(peso=0.12, valor=None)
        T2 = Nota(peso=0.28, valor=None)
        trabalhos_que_quero = [T1, T2]
        
        boletim = Boletim(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho)
        
        
        assert len(boletim.provas_que_quero()) == len(provas_que_quero)
        assert [boletim.provas_que_quero()[i] == provas_que_quero[i] for i in range(len(provas_que_quero))]
        
    def test_trabalhos_que_quero(self):
        P1 = Nota(peso=0.24, valor=1.0)
        provas_que_tenho = [P1]
        
        trabalhos_que_tenho = []
        
        P2 = Nota(peso=0.36, valor=None)
        provas_que_quero = [P2]
        
        T1 = Nota(peso=0.12, valor=None)
        T2 = Nota(peso=0.28, valor=None)
        trabalhos_que_quero = [T1, T2]
        
        boletim = Boletim(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho)
        
        
        assert len(boletim.trabalhos_que_quero()) == len(trabalhos_que_quero)
        assert [boletim.trabalhos_que_quero()[i] == trabalhos_que_quero[i] for i in range(len(trabalhos_que_quero))]