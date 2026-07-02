from typing import List, Optional

from src.shared.domain.entities.curso import Curso
from src.shared.domain.repositories.curso_repository_interface import ICursoRepository


class CursoRepositoryMock(ICursoRepository):

    def __init__(self):
        self.cursos = [
            Curso(código="ECM", nome="Engenharia de Computação"),
            Curso(código="ADM", nome="Administração"),
            Curso(código="CIC", nome="Ciência da Computação"),
        ]

    def create_curso(self, curso: Curso) -> Optional[Curso]:
        self.cursos.append(curso)
        return curso

    def get_curso(self, código: str) -> Optional[Curso]:
        return next((c for c in self.cursos if c.código == código), None)

    def update_curso(self, curso: Curso) -> Optional[Curso]:
        for i, c in enumerate(self.cursos):
            if c.código == curso.código:
                self.cursos[i] = curso
                return curso
        return None

    def delete_curso(self, código: str) -> Optional[Curso]:
        for i, c in enumerate(self.cursos):
            if c.código == código:
                return self.cursos.pop(i)
        return None

    def get_all_cursos(self) -> List[Curso]:
        return list(self.cursos)
