from src.shared.domain.entities.disciplina import Disciplina
from src.shared.domain.repositories.disciplina_repository_interface import IDisciplinaRepository
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound


class DeleteCustomDisciplinaUsecase:

    def __init__(self, repository: IDisciplinaRepository):
        self.repository = repository

    def __call__(self, code: str) -> Disciplina:
        existing = self.repository.get_disciplina(code)
        if existing is None:
            raise NoItemsFound(message=f"disciplina {code}")

        if not existing.is_custom:
            raise ForbiddenAction(message="catalog disciplina")

        removed = self.repository.delete_disciplina(code)
        if removed is None:
            raise NoItemsFound(message=f"disciplina {code}")
        return removed
