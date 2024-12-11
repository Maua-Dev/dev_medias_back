import abc
from typing import List
from src.shared.domain.entities.nota import Nota

from src.shared.helpers.errors.domain_errors import EntityParameterError
from src.shared.helpers.errors.function_errors import FunctionInputError


class Boletim(abc.ABC):
    tenho: List[Nota]	
    quero: List[Nota]
    idx_tenho: int # idx que representa onde se iniciam os trabalhos que tenho no atributo `tenho` 
    idx_quero: int # idx que representa onde se iniciam os trabalhos que quero no atributo `quero`

    def __init__(self, provas_que_tenho: List[Nota] = [], provas_que_quero: List[Nota] = [], trabalhos_que_tenho: List[Nota] = [], trabalhos_que_quero: List[Nota] = []):
        if not self.valida_lista_de_notas(provas_que_tenho):
            raise EntityParameterError("Lista de provas_que_tenho deve ser do tipo List[Nota]")
        if not self.valida_lista_de_notas(provas_que_quero):
            raise EntityParameterError("Lista de provas_que_quero deve ser do tipo List[Nota]")
        if not self.valida_lista_de_notas(trabalhos_que_tenho):
            raise EntityParameterError("Lista de trabalhos_que_tenho deve ser do tipo List[Nota]")
        if not self.valida_lista_de_notas(trabalhos_que_quero):
            raise EntityParameterError("Lista de trabalhos_que_quero deve ser do tipo List[Nota]")
        
        self.tenho = provas_que_tenho + trabalhos_que_tenho
        self.quero = provas_que_quero + trabalhos_que_quero
        
        self.idx_tenho = len(provas_que_tenho)
        self.idx_quero = len(provas_que_quero)       
        
        if(not self.valida_pesos(provas=self.provas(), trabalhos=self.trabalhos())):
            raise EntityParameterError("A soma dos pesos das notas passadas deve ser 1")
        
    def provas(self) -> List[Nota]:
        result = self.tenho[:self.idx_tenho] + self.quero[:self.idx_quero]
        return result
    
    def trabalhos(self) -> List[Nota]:
        result = self.tenho[self.idx_tenho:] + self.quero[self.idx_quero:]
        return result
    
    def provas_que_quero(self) -> List[Nota]:
        return self.quero[:self.idx_quero]

    def trabalhos_que_quero(self) -> List[Nota]:
        return self.quero[self.idx_quero:]
    
    def media_provas(self) -> float:
        if(self.valida_preenchimento(self.provas()) == False):
            raise FunctionInputError("media_provas", "O valor das provas devem estar preenchidos")
        decimal_value = sum(map(lambda x: x.valor * x.peso, self.provas()))
        if decimal_value * 100 % 1 > 0.9999999999:
            decimal_value = round(decimal_value, ndigits=2)
        return decimal_value

    
    def media_trabalhos(self) -> float:
        if(self.valida_preenchimento(self.trabalhos()) == False):
            raise FunctionInputError("media_trabalhos", "O valor dos trabalhos devem estar preenchidos")
        decimal_value = sum(map(lambda x: x.valor * x.peso, self.trabalhos()))
        if decimal_value * 100 % 1 > 0.9999999999:
            decimal_value = round(decimal_value, ndigits=2)
        return decimal_value

    def media_final(self) -> float:
        
        def arredondar_media(media):
            # Multiplica a média por 10 para trabalhar com o centésimo
            media_x10 = media * 10
            # Separa o valor inteiro e a parte decimal da multiplicação
            inteiro = int(media_x10)
            decimal = media_x10 - inteiro

            # Verifica se o centésimo é maior ou igual a 0.5
            if decimal >= 0.5:
                return round(media_x10) / 10
            else:
                return inteiro / 10
        
        return arredondar_media(self.media_provas() + self.media_trabalhos())
        
        
    
    @staticmethod
    def media_final_externo(idx_tenho: int, idx_quero: int, tenho: List[Nota], quero: List[Nota]) -> float:
        boletim = Boletim(
            provas_que_quero=quero[:idx_quero],
            provas_que_tenho=tenho[:idx_tenho],
            trabalhos_que_quero=quero[idx_quero:],
            trabalhos_que_tenho=tenho[idx_tenho:]
        )              
        return boletim.media_final()

    @staticmethod
    def valida_lista_de_notas(notas: List[Nota]) -> bool:
        if type(notas) != list:
            return False
        for nota in notas:
            if type(nota) != Nota:
                return False
        return True
    
    @staticmethod
    def valida_preenchimento(notas: List[Nota]) -> bool:
        if type(notas) != list:
            return False
        for nota in notas:
            if type(nota) != Nota:
                return False
            if nota.valor == None:
                return False
        return True
    
    @staticmethod
    def valida_pesos(provas: List[Nota], trabalhos: List[Nota]) -> bool:
        pesos = round(number=sum([prova.peso for prova in provas]) + sum([trabalho.peso for trabalho in trabalhos]), ndigits=2)
        if pesos != 1.00:
            return False
        return True
    
    def __str__(self):
        string = "Provas: [\nTenho: [ "
        
        for idx in range(self.idx_tenho - 1):
            string += str(self.tenho[idx]) + ", "
        last_prova_tenho = self.idx_tenho - 1
        if last_prova_tenho >= 0:
            string += str(self.tenho[last_prova_tenho])
        string += " ]\nQuero: [ "
        
        for idx in range(self.idx_quero - 1):
            string += str(self.quero[idx]) + ", "
        last_prova_quero = self.idx_quero - 1
        if last_prova_quero >= 0:
            string += str(self.quero[last_prova_quero])
        string += " ]\n]\n"
        
        string += "Trabalhos: [ "
        for idx in range(self.idx_tenho, len(self.tenho) - 1):
            string += str(self.tenho[idx]) + ", "
        last_trabalho_tenho = len(self.tenho) - 1
        if self.idx_tenho <= last_trabalho_tenho:
            string += str(self.tenho[last_trabalho_tenho])
        string += " ]\nQuero: [ "
        
        for idx in range(self.idx_quero, len(self.quero) - 1):
            string += str(self.quero[idx]) + ", "
        last_trabalho_quero = len(self.quero) - 1
        if self.idx_quero <= last_trabalho_quero:
            string += str(self.quero[last_trabalho_quero])
        string += " ]\n]\n"
        
        return string