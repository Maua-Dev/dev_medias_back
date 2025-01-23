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

class CalculateMeanViewmodel:
    media: float
    message: str

    def __init__(self, media: float):
        self.media = media
        self.message = "Média calculada com sucesso"

    def to_dict(self):
        return {
            'media': self.media,
            'message': self.message
        }
            

