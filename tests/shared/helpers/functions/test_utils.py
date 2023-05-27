import pytest
from src.shared.domain.entities.nota import Nota
from src.shared.helpers.errors.function_errors import FunctionInputError
from src.shared.helpers.functions.utils import Utils


class TestUtils:
    def test_media_aritimetica(self):
        l = [Nota(0.1, 5), Nota(0.1, 4), Nota(0.1, 2), Nota(0.2, 10)]
        assert Utils.media_aritimetica(l) == 5.25
        
    def test_media_aritimetica_lista_vazia(self):
        l = []
        with pytest.raises(FunctionInputError):
            Utils.media_aritimetica(l)
            
    def test_media(self):
        l = [Nota(0.2, 5), Nota(0.3, 4), Nota(0.1, 2), Nota(0.4, 10)]
        assert Utils.media(l) == 6.4
    
    def test_media_soma_dos_pesos_diferente_de_1(self):
        l = [Nota(0.2, 5), Nota(0.3, 4), Nota(0.1, 2), Nota(0.5, 10)]
        with pytest.raises(FunctionInputError):
            Utils.media(l)
            
    def test_desvio_padrao(self):
        l = [Nota(0.2, 5), Nota(0.3, 4), Nota(0.1, 2), Nota(0.4, 10)]
        assert round(Utils.desvio_padrao(l), 2) == 3.40
        
    def test_distancia_entre_notas_true(self):
        l = [Nota(0.2, 5), Nota(0.3, 4), Nota(0.1, 3), Nota(0.4, 2)]
        assert Utils.distancia_entre_notas(l, 1.5) == True
        
    def test_distancia_entre_notas_false(self):
        l = [Nota(0.2, 10), Nota(0.3, 4), Nota(0.1, 3), Nota(0.4, 2)]
        assert Utils.distancia_entre_notas(l, 1.5) == False
        
    def test_minimo_valor_no_dominio(self):
        notas_que_tenho = [Nota(0.1, 5), Nota(0.15, 4), Nota(0.05, 3), Nota(0.2, 2)]
        notas_que_quero = [Nota(0.1, 10), Nota(0.10, 4), Nota(0.05, 3), Nota(0.2, 2)]
        assert Utils.minimo_valor_no_dominio(notas_que_tenho=notas_que_tenho, notas_que_quero=notas_que_quero, peso_especifico=0.1, media_desejada=7, erro_max=0.5, distancia_max=1.5) == 7.5
    
    def test_minimo_valor_no_dominio_notas_que_quero_vazia(self):
        notas_que_tenho = [Nota(0.2, 10), Nota(0.3, 7), Nota(0.1, 5), Nota(0.3, 2)]
        notas_que_quero = []
        assert Utils.minimo_valor_no_dominio(notas_que_quero=notas_que_quero, notas_que_tenho =notas_que_tenho, peso_especifico=0.1, media_desejada=6, erro_max=0.5, distancia_max=1.5) == 3.5
        
    def test_minimo_valor_no_dominio_notas_que_quero_minimo_valor_0(self):
        notas_que_tenho = [Nota(0.2, 10), Nota(0.3, 10), Nota(0.1, 5), Nota(0.3, 2)]
        notas_que_quero = []
        assert Utils.minimo_valor_no_dominio(notas_que_quero=notas_que_quero, notas_que_tenho =notas_que_tenho, peso_especifico=0.1, media_desejada=6, erro_max=0.5, distancia_max=1.5) == 0
        
    def test_minimo_valor_no_dominio_impossivel_tirar_media_desejada(self):
        notas_que_tenho = [Nota(0.2, 10), Nota(0.3, 0), Nota(0.1, 5), Nota(0.3, 2)]
        notas_que_quero = []
        assert Utils.minimo_valor_no_dominio(notas_que_quero=notas_que_quero, notas_que_tenho =notas_que_tenho, peso_especifico=0.1, media_desejada=9, erro_max=0.5, distancia_max=1.5) == -1
        
    def test_maximo_valor_no_dominio(self):
        notas_que_tenho = [Nota(0.1, 5), Nota(0.15, 10), Nota(0.05, 3), Nota(0.2, 10)]
        notas_que_quero = [Nota(0.1, 10), Nota(0.10, 10), Nota(0.05, 3), Nota(0.2, 2)]
        assert Utils.maximo_valor_no_dominio(notas_que_quero=notas_que_quero, notas_que_tenho =notas_que_tenho, peso_especifico=0.1, media_desejada=6, erro_max=0.5, distancia_max=1.5) == 5.5
        
    def test_maximo_valor_no_dominio_notas_que_quero_vazia(self):
        notas_que_tenho = [Nota(0.2, 10), Nota(0.3, 10), Nota(0.1, 5), Nota(0.3, 2)]
        notas_que_quero = []
        assert Utils.maximo_valor_no_dominio(notas_que_quero=notas_que_quero, notas_que_tenho =notas_que_tenho, peso_especifico=0.1, media_desejada=6, erro_max=0.5, distancia_max=1.5) == 4
        
    def test_maximo_valor_10(self):
        notas_que_tenho = [Nota(0.1, 5), Nota(0.15, 0), Nota(0.05, 0), Nota(0.2, 0)]
        notas_que_quero = [Nota(0.1, 10), Nota(0.10, 0), Nota(0.05, 0), Nota(0.2, 2)]
        assert Utils.maximo_valor_no_dominio(notas_que_quero=notas_que_quero, notas_que_tenho =notas_que_tenho, peso_especifico=0.1, media_desejada=6, erro_max=0.5, distancia_max=1.5) == 10