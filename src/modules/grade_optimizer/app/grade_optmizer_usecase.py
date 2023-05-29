from typing import List

from src.shared.domain.entities.nota import Nota
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.function_errors import FunctionInputError
from src.shared.helpers.errors.usecase_errors import InvalidInput
from src.shared.solucionador import Solucionador


class GradeOptimizerUsecase:
    def __init__(self):
        pass

    def __call__(self, notas_que_tenho: List[Nota], notas_que_quero: List[Nota], media_desejada: float) -> List[Nota]:
        if(len(notas_que_quero) == 0):
            raise InvalidInput("notas_que_quero", "Não pode ser uma lista vazia")
        
        if(media_desejada < Nota.DOMINIO_DE_NOTAS[0] or media_desejada > Nota.DOMINIO_DE_NOTAS[-1]):
            raise InvalidInput("media_desejada", "Deve estar compreendida entre 0 e 10")
        
        if round(sum(map(lambda x: x.peso, notas_que_tenho+notas_que_quero)), 2) != 1.00:
            raise FunctionInputError("media", "A soma dos pesos deve ser 1")
        
        return Solucionador.algoritmo(notas_que_tenho, notas_que_quero, media_desejada)