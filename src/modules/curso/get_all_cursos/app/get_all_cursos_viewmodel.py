from src.shared.domain.entities.curso import Curso


class GetAllCursosViewmodel:
    def __init__(self, cursos: list[Curso]):
        self.cursos = cursos

    def to_dict(self) -> list[dict]:
        return [curso.model_dump(mode='json') for curso in self.cursos]
