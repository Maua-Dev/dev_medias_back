import abc
from random import shuffle
from typing import List, Tuple

from src.shared.helpers.errors.domain_errors import EntityError, EntityParameterError


class Nota(abc.ABC):
    peso: float # representa o peso da nota na matéria
    valor: float = None # representa o valor da nota
    dominio_da_nota: List[float] # representa o domínio de notas possíveis para uma nota em específico
    DOMINIO_DE_NOTAS = list(map(lambda x: x/ 2, range(0, 21)))

    def __init__(self, peso: float = None, valor: float = None):
        nota_valida, msg = self.valida_valor(valor)
        if (not nota_valida and valor != None):
            raise EntityParameterError(msg)
        self.valor = valor

        peso_valido, msg = self.valida_peso(peso)
        if (not peso_valido):
            raise EntityParameterError(msg)
        self.peso = peso

        self.dominio_da_nota = self.DOMINIO_DE_NOTAS.copy()

    def randomiza_dominio(self) -> None:
        shuffle(self.dominio_da_nota)

    def limita_dominio(self, valor_minimo: float, valor_maximo: float) -> None:
        dominio_valido, msg = self.valida_limitacao_de_dominio(self.dominio_da_nota, valor_minimo, valor_maximo)
        if (not dominio_valido):
            raise EntityParameterError(msg)
        self.dominio_da_nota = [nota for nota in self.dominio_da_nota if nota >= valor_minimo and nota <= valor_maximo]

    def restaura_dominio(self) -> None:
        self.dominio_da_nota = Nota.DOMINIO_DE_NOTAS.copy()

    @staticmethod
    def valida_limitacao_de_dominio(dominio_a_ser_limitado: List[float], valor_minimo: float, valor_maximo: float) -> \
    Tuple[bool, str]:
        if (valor_maximo < valor_minimo):
            return (False, f"Valor mínimo {valor_minimo} deve ser menor que valor máximo {valor_maximo}")

        valor_minimo_valido, msg = Nota.valida_valor(valor_minimo)
        if (not valor_minimo_valido):
            return (valor_minimo_valido, msg)

        valor_maximo_valido, msg = Nota.valida_valor(valor_maximo)
        if (not valor_maximo_valido):
            return (valor_maximo_valido, msg)

        elif (len(dominio_a_ser_limitado) != len(Nota.DOMINIO_DE_NOTAS)):
            return (False, f"Domínio da nota já foi limitado")
        elif (dominio_a_ser_limitado != Nota.DOMINIO_DE_NOTAS):
            return (False, f"Domínio da nota já foi embaralhado")
        else:
            return (True, '')

    @staticmethod
    def valida_valor(valor: int) -> Tuple[bool, str]:
        if (type(valor) not in [float, int]):
            return (False, f"Valor de nota {valor} deve ser um número")
        if (valor not in Nota.DOMINIO_DE_NOTAS):
            return (False, f"Valor de nota {valor} deve estar entre 0 e 10, variando de 0.5 em 0.5")
        return (True, '')

    @staticmethod
    def valida_peso(peso: int) -> Tuple[bool, str]:
        if (peso is None):
            return (False, f"Peso {peso} não pode ser nulo")
        elif (type(peso) != float):
            return (False, f"Peso {peso} deve ser um número")
        elif (peso < 0):
            return (False, f"Peso {peso} não pode ser menor que 0")
        elif (peso > 1):
            return (False, f"Peso {peso} não pode ser maior que 1")
        return (True, '')

    def __str__(self):
        return f"(Valor: {self.valor}, Peso: {self.peso})"
