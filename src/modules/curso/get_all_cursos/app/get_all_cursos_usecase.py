from src.shared.domain.entities.curso import Curso
from src.shared.domain.repositories.curso_repository_interface import ICursoRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class GetAllCursosUsecase:

    def __init__(self, repository: ICursoRepository):
        self.repository = repository

    def __call__(self) -> list[Curso]:
        cursos = self.repository.get_all_cursos()

        if not cursos:
            raise NoItemsFound(message='cursos')

        return cursos
