from src.shared.domain.entities.boletim import Boletim
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
    boletim: Boletim

    def __init__(self, boletim: Boletim):
        self.boletim = boletim

    def to_dict(self):
            
        if all([nota.valor != None for nota in self.boletim.quero]):
            return {
                'notas': {
                    'provas': [NotaViewmodel(nota).to_dict() for nota in self.boletim.provas_que_quero()],
                    'trabalhos': [NotaViewmodel(nota).to_dict() for nota in self.boletim.trabalhos_que_quero()],
                },
                'message': "O algoritmo retornou uma combinação válida de notas"
            }
        else:
            return {
                'notas': {
                    'provas': [],
                    'trabalhos': [],
                },
                'message': "O algoritmo não encontrou uma combinação possível de notas"
            }

