from src.shared.domain.entities.curso import Curso


class CreateCursoViewmodel:
    def __init__(self, curso: Curso):
        self.curso = curso

    def to_dict(self) -> dict:
        return self.curso.model_dump(mode='json')
