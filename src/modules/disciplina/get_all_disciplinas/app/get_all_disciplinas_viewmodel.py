from src.shared.domain.entities.disciplina import Disciplina


class GetAllDisciplinasViewmodel:
    def __init__(self, disciplinas: list[Disciplina]):
        self.disciplinas = disciplinas

    def to_dict(self) -> list[dict]:
        return [disciplina.model_dump(mode="json") for disciplina in self.disciplinas]
