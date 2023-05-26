from typing import List

from src.shared.domain.entities.nota import Nota
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.solucionador import Solucionador


class GradeOptimizerUsecase:
    def __init__(self):
        pass

    def __call__(self, notas_que_tenho: List[Nota], notas_que_quero: List[Nota], media_desejada: float) -> List[Nota]:

        return Solucionador.algoritmo(notas_que_tenho, notas_que_quero, media_desejada)