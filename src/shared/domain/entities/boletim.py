import abc
from typing import List, Tuple
from src.shared.domain.entities.conjunto_de_notas import ConjuntoDeNotas
from src.shared.domain.entities.nota import Nota

from src.shared.helpers.errors.domain_errors import EntityError, EntityParameterError
from src.shared.helpers.errors.function_errors import FunctionInputError
from src.shared.helpers.functions.utils import Utils


class Boletim(abc.ABC):
    provas: ConjuntoDeNotas
    trabalhos: ConjuntoDeNotas

    def __init__(self, provas: ConjuntoDeNotas, trabalhos: ConjuntoDeNotas):
        if(not self.valida_notas(provas)):
            raise EntityParameterError("Lista de provas deve ser do tipo ConjuntoDeNotas")
        
        if(not self.valida_notas(trabalhos)):
            raise EntityParameterError("Lista de trabalhos deve ser do tipo ConjuntoDeNotas")
        
        if(not self.valida_pesos(provas=provas, trabalhos=trabalhos)):
            raise FunctionInputError("media", "A soma dos pesos deve ser 1")
        
        self.provas = provas
        self.trabalhos = trabalhos
        

    def media_final(self):
        return self.provas.media() + self.trabalhos.media()

    @staticmethod
    def valida_notas(notas: List[Nota]) -> bool:
        if type(notas) != ConjuntoDeNotas:
            return False
        return True
    
    @staticmethod
    def valida_pesos(provas: ConjuntoDeNotas, trabalhos: ConjuntoDeNotas) -> bool:
        pesos = round(number=sum([prova.peso for prova in provas.tenho+provas.quero]) + sum([trabalho.peso for trabalho in trabalhos.tenho+trabalhos.quero]), ndigits=2)
        if pesos != 1.00:
            return False
        return True
    
    def __str__(self):
        string = "Provas: [ "
        string += self.provas.__str__() + " ]\n"
        
        string += "Trabalhos: [ "
        string += self.trabalhos.__str__() + " ]\n"
        
        return string