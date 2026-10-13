from src.shared.domain.entities.disciplina import Disciplina


class CreateCustomDisciplinaViewmodel:
    def __init__(self, disciplina: Disciplina):
        self.disciplina = disciplina

    def to_dict(self) -> dict:
        return self.disciplina.model_dump(mode="json")
