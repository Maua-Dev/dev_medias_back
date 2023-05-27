from src.shared.domain.entities.nota import Nota
from src.shared.helpers.errors.domain_errors import EntityParameterError


class Test_Nota:
    def test_nota(self):
        nota = Nota(peso=0.12, valor=6.0)
        assert nota.peso == 0.12
        assert nota.valor == 6.0
        assert nota.dominio_da_nota == Nota.DOMINIO_DE_NOTAS
        
    def test_nota_valor_nulo(self):
        nota = Nota(peso=0.12, valor=None)
        assert nota.peso == 0.12
        assert nota.valor == None
        
    def test_nota_valor_tipo_errado(self):
        try:
            Nota(peso=0.12, valor='6.0')
            assert False
        except EntityParameterError as e:
            assert str(e) == "Valor de nota 6.0 deve ser um número"
            
    def test_nota_valor_fora_do_dominio(self):
        try:
            Nota(peso=0.12, valor=6.1)
            assert False
        except EntityParameterError as e:
            assert str(e) == "Valor de nota 6.1 deve estar entre 0 e 10, variando de 0.5 em 0.5"
            
    def test_nota_peso_nulo(self):
        try:
            Nota(peso=None, valor=6.0)
            assert False
        except EntityParameterError as e:
            assert str(e) == "Peso None não pode ser nulo"
    
    def test_nota_peso_tipo_errado(self):
        try:
            Nota(peso='0.12', valor=6.0)
            assert False
        except EntityParameterError as e:
            assert str(e) == "Peso 0.12 deve ser um número"
    
    def test_nota_peso_menor_que_zero(self):
        try:
            Nota(peso=-0.12, valor=6.0)
            assert False
        except EntityParameterError as e:
            assert str(e) == "Peso -0.12 não pode ser menor que 0"
    
    def test_nota_peso_maior_que_um(self):
        try:
            Nota(peso=1.12, valor=6.0)
            assert False
        except EntityParameterError as e:
            assert str(e) == "Peso 1.12 não pode ser maior que 1"
            
    def test_nota_randomiza_dominio(self):
        nota = Nota(peso=0.12, valor=6.0)
        nota.randomiza_dominio()
        
        assert nota.peso == 0.12
        assert nota.valor == 6.0
        assert nota.dominio_da_nota != Nota.DOMINIO_DE_NOTAS
        assert len(nota.dominio_da_nota) == len(Nota.DOMINIO_DE_NOTAS)
        assert all([i in nota.dominio_da_nota for i in Nota.DOMINIO_DE_NOTAS])
        
    def test_nota_limita_dominio(self):
        nota = Nota(peso=0.12, valor=6.0)
        nota.limita_dominio(0,Nota.DOMINIO_DE_NOTAS[9 ])
        
        assert nota.peso == 0.12
        assert nota.valor == 6.0
        assert nota.dominio_da_nota != Nota.DOMINIO_DE_NOTAS
        assert len(nota.dominio_da_nota) == 10
        assert all([i in nota.dominio_da_nota for i in Nota.DOMINIO_DE_NOTAS[:10]])
        
    def test_nota_limita_dominio_valor_maximo_menor_que_minimo(self):
        valor_minimo = Nota.DOMINIO_DE_NOTAS[9]
        valor_maximo = Nota.DOMINIO_DE_NOTAS[0]
        
        try:
            nota = Nota(peso=0.12, valor=6.0)
            
            
            nota.limita_dominio(valor_minimo, valor_maximo)
            assert False
        except EntityParameterError as e:
            assert str(e) == f"Valor mínimo {valor_minimo} deve ser menor que valor máximo {valor_maximo}"
            
    def test_nota_limita_dominio_valor_minimo_invalido(self):
        valor_minimo = -1
        valor_maximo = Nota.DOMINIO_DE_NOTAS[0]
        
        try:
            nota = Nota(peso=0.12, valor=6.0)
            
            
            nota.limita_dominio(valor_minimo, valor_maximo)
            assert False
        except EntityParameterError as e:
            assert str(e) == f"Valor de nota -1 deve estar entre 0 e 10, variando de 0.5 em 0.5"
            
    def test_nota_limita_dominio_valor_maximo_invalido(self):
        valor_minimo = Nota.DOMINIO_DE_NOTAS[9]
        valor_maximo = 11
        
        try:
            nota = Nota(peso=0.12, valor=6.0)
            
            
            nota.limita_dominio(valor_minimo, valor_maximo)
            assert False
        except EntityParameterError as e:
            assert str(e) == f"Valor de nota 11 deve estar entre 0 e 10, variando de 0.5 em 0.5"
    
    def test_nota_limita_dominio_ja_limitado(self):
        valor_minimo = Nota.DOMINIO_DE_NOTAS[0]
        valor_maximo = Nota.DOMINIO_DE_NOTAS[9]
        
        nota = Nota(peso=0.12, valor=6.0)
        nota.limita_dominio(valor_minimo, valor_maximo)
        
        try:
            nota.limita_dominio(valor_minimo, valor_maximo)
            assert False
        except EntityParameterError as e:
            assert str(e) == "Domínio da nota já foi limitado"
    
    def test_nota_limita_dominio_ja_randomizado(self):
        nota = Nota(peso=0.12, valor=6.0)
        nota.randomiza_dominio()
        
        try:
            nota.limita_dominio(0, Nota.DOMINIO_DE_NOTAS[9])
            assert False
        except EntityParameterError as e:
            assert str(e) == "Domínio da nota já foi embaralhado"