import abc
from typing import List
from src.shared.domain.entities.nota import Nota

from src.shared.helpers.errors.domain_errors import EntityParameterError
from src.shared.helpers.functions.utils import Utils


class ConjuntoDeNotas(abc.ABC):
    tenho: List[Nota]
    quero: List[Nota]

    def __init__(self, tenho: List[Nota] = [], quero: List[Nota] = []):
        if(not self.valida_tenho(notas=tenho)):
            raise EntityParameterError("Conjunto de notas que tenho deve ser do tipo Nota, com peso e valor")
        self.tenho = tenho
        
        if(not self.valida_quero(notas=quero)):
            raise EntityParameterError("Conjunto de notas que tenho deve ser do tipo Nota, com peso e sem valor")
        self.quero = quero

    @staticmethod
    def valida_tenho(notas: List[Nota]) -> bool:
        for nota in notas:
            if type(nota) != Nota:
                return False
            if nota.valor == None:
                return False
        return True
    
    @staticmethod
    def valida_quero(notas: List[Nota]) -> bool:
        for nota in notas:
            if type(nota) != Nota:
                return False
            if nota.valor != None:
                return False
        return True
        
    def media(self):
        return round(number=sum(map(lambda x: x.valor * x.peso, (self.tenho + self.quero))), ndigits=1)
    
    def __str__(self):
        string = "Tenho: ["
        for idx in range(len(self.tenho)-1):
            string += str(self.tenho[idx]) + ", "
        string += str(self.tenho[-1]) + "]\n"
        
        string += "Quero: ["
        for idx in range(len(self.quero)-1):
            string += str(self.quero[idx]) + ", "
        string += str(self.quero[-1]) + "]"
        
        return string