from src.shared.domain.entities.curso import Curso
from src.shared.domain.repositories.curso_repository_interface import ICursoRepository
from src.shared.helpers.errors.usecase_errors import DuplicatedItem


class CreateCursoUsecase:

    def __init__(self, repository: ICursoRepository):
        self.repository = repository

    def __call__(self, código: str, nome: str) -> Curso:
        existing_curso = self.repository.get_curso(código)

        if existing_curso is not None:
            raise DuplicatedItem(message='código')

        curso = Curso(código=código, nome=nome)

        return self.repository.create_curso(curso)
