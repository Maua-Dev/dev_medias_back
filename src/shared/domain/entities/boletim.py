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
        if not self.valida_tenho(provas_que_tenho):
            raise EntityParameterError("Lista de provas_que_tenho deve ser do tipo List[Nota] e todas as notas devem ter valor")
        if not self.valida_quero(provas_que_quero):
            raise EntityParameterError("Lista de provas_que_quero deve ser do tipo List[Nota] e todas as notas devem ter valor None")
        if not self.valida_tenho(trabalhos_que_tenho):
            raise EntityParameterError("Lista de trabalhos_que_tenho deve ser do tipo List[Nota] e todas as notas devem ter valor")
        if not self.valida_quero(trabalhos_que_quero):
            raise EntityParameterError("Lista de trabalhos_que_quero deve ser do tipo List[Nota] e todas as notas devem ter valor None")
        
        self.tenho = provas_que_tenho + trabalhos_que_tenho
        self.quero = provas_que_quero + trabalhos_que_quero
        
        self.idx_tenho = len(provas_que_tenho)
        self.idx_quero = len(provas_que_quero)       
        
        if(not self.valida_pesos(provas=self.provas(), trabalhos=self.trabalhos())):
            raise FunctionInputError("media", "A soma dos pesos deve ser 1")
        
        

    def media_final(self) -> float:
        return self.provas.media() + self.trabalhos.media()

    def provas(self) -> List[Nota]:
        result = self.tenho[:self.idx_tenho] + self.quero[:self.idx_quero]
        return result
    
    def trabalhos(self) -> List[Nota]:
        result = self.tenho[self.idx_tenho:] + self.quero[self.idx_quero:]
        return result
    
    def media_provas(self) -> float:
        return round(sum(map(lambda x: x.valor * x.peso, self.provas())), ndigits=1)
    
    def media_trabalhos(self) -> float:
        return round(sum(map(lambda x: x.valor * x.peso, self.trabalhos())), ndigits=1)
    
    def media_final(self) -> float:
        return round(self.media_provas() + self.media_trabalhos(), ndigits=1)

    @staticmethod
    def valida_tenho(notas: List[Nota]) -> bool:
        if type(notas) != list:
            return False
        for nota in notas:
            if type(nota) != Nota:
                return False
            if nota.valor == None:
                return False
        return True
    
    @staticmethod
    def valida_quero(notas: List[Nota]) -> bool:
        if type(notas) != list:
            return False
        for nota in notas:
            if type(nota) != Nota:
                return False
            if nota.valor != None:
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
        string += str(self.tenho[self.idx_tenho - 1]) + " ]\nQuero: [ "
        for idx in range(self.idx_quero - 1):
            string += str(self.quero[idx]) + ", "
        string += str(self.quero[self.idx_quero - 1]) + " ]\n]\n"
        
        string += "Trabalhos: [ "
        for idx in range(self.idx_tenho, len(self.tenho) - 1):
            string += str(self.tenho[idx]) + ", "
        string += str(self.tenho[len(self.tenho) - 1]) + " ]\nQuero: [ "
        for idx in range(self.idx_quero, len(self.quero) - 1):
            string += str(self.quero[idx]) + ", "
        string += str(self.quero[len(self.quero) - 1]) + " ]\n]\n"
        
        return string