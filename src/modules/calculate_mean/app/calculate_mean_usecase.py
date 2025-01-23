from typing import List
from src.shared.domain.entities.boletim import Boletim

from src.shared.domain.entities.nota import Nota
from src.shared.helpers.errors.function_errors import FunctionInputError
from src.shared.helpers.errors.usecase_errors import CombinationNotFound, InvalidInput
from src.shared.solucionador import Solucionador


class CalculateMeanUsecase:
    def __init__(self):
        pass

    def __call__(self, peso_prova: float, peso_trabalho: float, provas_que_tenho: List[Nota], trabalhos_que_tenho: List[Nota]) -> float:
        if(len(provas_que_tenho) + len(trabalhos_que_tenho)== 0):
            raise InvalidInput("provas_que_tenho e trabalhos_que_tenho", "Não podem ser listas vazias")
        
        # verificando lista de provas_que_tenho e trabalhos_que_tenho
        if (Boletim.valida_preenchimento(provas_que_tenho) == False):
            raise FunctionInputError("CalculateMeanUsecase", "O valor das provas que tenho devem estar preenchidos")
        
        
        if (Boletim.valida_preenchimento(trabalhos_que_tenho) == False):
            raise FunctionInputError("CalculateMeanUsecase", "O valor dos trabalhos que tenho devem estar preenchidos")
        
        # validação dos pesos feita pelo próprio boletim
        boletim = Boletim(peso_prova=peso_prova, peso_trabalho=peso_trabalho, provas_que_quero=[], provas_que_tenho=provas_que_tenho, trabalhos_que_quero=[], trabalhos_que_tenho=trabalhos_que_tenho)
        
        media_final = boletim.media_final()
        
        return media_final
