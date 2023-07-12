import math
from typing import List

from src.shared.domain.entities.nota import Nota
from src.shared.helpers.errors.function_errors import FunctionInputError


class Utils:

    @staticmethod
    def print_lista_de_notas(l: List[Nota]):
        if (len(l) == 0):
            print("[]")
            return
        print("[", end=' ')
        for idx in range(len(l) - 1):
            print(l[idx], end=', ')
        print(l[-1], end=' ]')

    @staticmethod
    def media_aritimetica(l: List[Nota]) -> float:
        if(len(l) == 0):
            raise FunctionInputError("media_aritimetica", "Lista de notas não pode ser vazia")
        return sum([nota.valor for nota in l]) / len(l)

    @staticmethod
    def media(l: List[Nota]) -> float:
        if round(sum(map(lambda x: x.peso, l)), 2) != 1.00:
            raise FunctionInputError("media", "A soma dos pesos deve ser 1")
        return sum(map(lambda x: x.valor * x.peso, l))

    @staticmethod
    def desvio_padrao(l: List[Nota]) -> float:
        media = Utils.media_aritimetica(l)
        return (sum(map(lambda x: (x.valor - media) ** 2, l)) / (len(l) - 1)) ** (1 / 2)

    @staticmethod
    def distancia_entre_notas(l: List[Nota], distancia_min: float) -> bool:
        media = Utils.media_aritimetica(l)
        return all(map(lambda x: abs(x.valor - media) <= distancia_min, l))

    @staticmethod
    def print_pesos_de_notas(l: List[Nota]):
        if (len(l) == 0):
            print("[]", end="")
            return
        print("[", end=' ')
        for idx in range(len(l) - 1):
            print(l[idx].peso, end=', ')
        print(l[-1].peso, end=' ]')

    @staticmethod
    def minimo_valor_no_dominio(notas_que_tenho: List[Nota], notas_que_quero: List[Nota], peso_especifico: float, media_desejada: float, erro_max: float, distancia_max: float, aumento_do_range: float = 0) -> float:
        A = media_desejada - sum([nota.peso * nota.valor for nota in notas_que_tenho])
        
        if(len(notas_que_quero) == 0):
            B = 0
        else: 
            B = ((len(notas_que_quero)+1) * (distancia_max+aumento_do_range))/(len(notas_que_quero)) # len(notas_que_quero) tira a nota `n_x`
        
        if(len(notas_que_quero) == 0):
            C = 0
        else:
            C = sum([nota.peso for nota in notas_que_quero])
        
        valor = math.ceil(2*((A-erro_max-B*C)/(C+peso_especifico)))/2
        if valor < Nota.DOMINIO_DE_NOTAS[0]: # 0
            return Nota.DOMINIO_DE_NOTAS[0]
        elif valor > Nota.DOMINIO_DE_NOTAS[-1]: # 10
            return -1
        return valor

    @staticmethod
    def maximo_valor_no_dominio(notas_que_tenho: List[Nota], notas_que_quero: List[Nota], peso_especifico: float, media_desejada: float, erro_max: float, distancia_max: float) -> float:
        A = media_desejada - sum([nota.peso * nota.valor for nota in notas_que_tenho])
        
        if(len(notas_que_quero) == 0):
            B = 0
        else:
            B = ((len(notas_que_quero)+1) * distancia_max)/(len(notas_que_quero)) # len(notas_que_quero) tira a nota `n_x`
        
        if(len(notas_que_quero) == 0):
            C = 0
        else:
            C = sum([nota.peso for nota in notas_que_quero])
        
        valor = math.floor(2*((A+erro_max+B*C)/(C+peso_especifico)))/2
        if valor > Nota.DOMINIO_DE_NOTAS[-1]: # 10
            return Nota.DOMINIO_DE_NOTAS[-1]
        elif valor < Nota.DOMINIO_DE_NOTAS[0]: #0
            return Nota.DOMINIO_DE_NOTAS[0]
        return valor