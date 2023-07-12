from typing import List
from src.shared.domain.entities.boletim import Boletim

from src.shared.domain.entities.nota import Nota
from src.shared.helpers.errors.function_errors import FunctionInputError
from src.shared.helpers.errors.usecase_errors import InvalidInput
from src.shared.solucionador import Solucionador


class GradeOptimizerUsecase:
    def __init__(self):
        pass

    def __call__(self, provas_que_tenho: List[Nota], provas_que_quero: List[Nota], trabalhos_que_tenho: List[Nota], trabalhos_que_quero: List[Nota],  media_desejada: float) -> List[Nota]:
        if(len(provas_que_quero) + len(trabalhos_que_quero)== 0):
            raise InvalidInput("provas_que_quero e trabalhos_que_quero", "Não podem ser listas vazias")
        
        if(media_desejada < Nota.DOMINIO_DE_NOTAS[0] or media_desejada > Nota.DOMINIO_DE_NOTAS[-1]):
            raise InvalidInput("media_desejada", "Deve estar compreendida entre 0 e 10")
        
        # validação dos pesos feita pelo próprio boletim
        boletim = Boletim(provas_que_quero=provas_que_quero, provas_que_tenho=provas_que_tenho, trabalhos_que_quero=trabalhos_que_quero, trabalhos_que_tenho=trabalhos_que_tenho)
        
        response = Solucionador.algoritmo(boletim=boletim, media_desejada=media_desejada)
        
        if(response == None):
            return boletim
        return response
