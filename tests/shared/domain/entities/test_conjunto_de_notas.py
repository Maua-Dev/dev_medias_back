import pytest
from src.shared.domain.entities.conjunto_de_notas import ConjuntoDeNotas
from src.shared.domain.entities.nota import Nota
from src.shared.helpers.errors.domain_errors import EntityParameterError


class Test_ConjuntoDeNotas:
    def test_conjunto_de_notas(self):
        P1 = Nota(peso=0.12, valor=6.0)
        P2 = Nota(peso=0.12, valor=None)
        P3 = Nota(peso=0.18, valor=None)
        P4 = Nota(peso=0.18, valor=None)
        
        notas_que_tenho = [P1]
        notas_que_quero = [P2, P3, P4]
        
        conjunto_de_notas = ConjuntoDeNotas(quero=notas_que_quero, tenho=notas_que_tenho)
        assert all([conjunto_de_notas.quero[i] == notas_que_quero[i] for i in range(len(notas_que_quero))])
        assert all([conjunto_de_notas.tenho[i] == notas_que_tenho[i] for i in range(len(notas_que_tenho))])

    def test_conjunto_de_notas_tenho_nao_nota(self):
        P1 = {
            "peso": 0.12,
            "valor": 6.0
        }
        P2 = Nota(peso=0.12, valor=None)
        P3 = Nota(peso=0.18, valor=None)
        P4 = Nota(peso=0.18, valor=None)
        
        notas_que_tenho = [P1]
        notas_que_quero = [P2, P3, P4]
        
        with pytest.raises(EntityParameterError):
            ConjuntoDeNotas(quero=notas_que_quero, tenho=notas_que_tenho)
    
    def test_conjunto_de_notas_tenho_nulo(self):
        P1 = Nota(peso=0.12, valor=None)
        P2 = Nota(peso=0.12, valor=None)
        P3 = Nota(peso=0.18, valor=None)
        P4 = Nota(peso=0.18, valor=None)
        
        notas_que_tenho = [P1]
        notas_que_quero = [P2, P3, P4]
        
        with pytest.raises(EntityParameterError):
            ConjuntoDeNotas(quero=notas_que_quero, tenho=notas_que_tenho)
    
    def test_conjunto_de_notas_quero_nao_nota(self):
        P1 = Nota(peso=0.12, valor=6.0)
        P2 = Nota(peso=0.12, valor=None)
        P3 = {
            "peso": 0.12,
            "valor": None
        }
        P4 = Nota(peso=0.18, valor=None)
        
        notas_que_tenho = [P1]
        notas_que_quero = [P2, P3, P4]
        
        with pytest.raises(EntityParameterError):
            ConjuntoDeNotas(quero=notas_que_quero, tenho=notas_que_tenho)
    
    def test_conjunto_de_notas_quero_nulo(self):
        P1 = Nota(peso=0.12, valor=6.0)
        P2 = Nota(peso=0.12, valor=None)
        P3 = Nota(peso=0.18, valor=4.0)
        P4 = Nota(peso=0.18, valor=None)
        
        notas_que_tenho = [P1]
        notas_que_quero = [P2, P3, P4]
        
        with pytest.raises(EntityParameterError):
            ConjuntoDeNotas(quero=notas_que_quero, tenho=notas_que_tenho)
            
    def test_conjunto_de_notas_media_floor(self):
        P1 = Nota(peso=0.12, valor=6.0)
        P2 = Nota(peso=0.12, valor=None)
        P3 = Nota(peso=0.18, valor=None)
        P4 = Nota(peso=0.18, valor=None)
        
        notas_que_tenho = [P1]
        notas_que_quero = [P2, P3, P4]
        
        conjunto_de_notas = ConjuntoDeNotas(quero=notas_que_quero, tenho=notas_que_tenho)
        conjunto_de_notas.quero[0].valor = 8.0
        conjunto_de_notas.quero[1].valor = 6.0
        conjunto_de_notas.quero[2].valor = 7.0
        assert conjunto_de_notas.media() == 4.0        
        
    def test_conjunto_de_notas_media_ceil(self):
        P1 = Nota(peso=0.12, valor=6.0)
        P2 = Nota(peso=0.12, valor=None)
        P3 = Nota(peso=0.18, valor=None)
        P4 = Nota(peso=0.18, valor=None)
        
        notas_que_tenho = [P1]
        notas_que_quero = [P2, P3, P4]
        
        conjunto_de_notas = ConjuntoDeNotas(quero=notas_que_quero, tenho=notas_que_tenho)
        conjunto_de_notas.quero[0].valor = 4.5
        conjunto_de_notas.quero[1].valor = 6.5
        conjunto_de_notas.quero[2].valor = 7.5
        assert conjunto_de_notas.media() == 3.8   