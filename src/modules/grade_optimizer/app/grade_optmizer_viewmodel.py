from typing import List
from src.shared.domain.entities.nota import Nota


class NotaViewmodel:
    valor: float
    peso: float

    def __init__(self, nota: Nota):
        self.valor = nota.valor
        self.peso = nota.peso

    def to_dict(self):
        return {
            'valor': self.valor,
            'peso': self.peso
        }

class GradeOptmizerViewmodel:
    user_id: int
    name: str
    email: str

    def __init__(self, combinacao_de_notas: List[Nota]):
        self.combinacao_de_notas = combinacao_de_notas

    def to_dict(self):
        return {
            'notas': [NotaViewmodel(nota).to_dict() for nota in self.combinacao_de_notas],
            'message': "the algorithm retrieved a possible combination of grades successfully"
        }