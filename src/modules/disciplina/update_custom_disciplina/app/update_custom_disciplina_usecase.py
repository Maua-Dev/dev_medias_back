from src.shared.domain.entities.disciplina import Disciplina
from src.shared.domain.repositories.disciplina_repository_interface import IDisciplinaRepository
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound


class UpdateCustomDisciplinaUsecase:

    def __init__(self, repository: IDisciplinaRepository):
        self.repository = repository

    def __call__(self, disciplina: Disciplina) -> Disciplina:
        existing = self.repository.get_disciplina(disciplina.code)
        if existing is None:
            raise NoItemsFound(message=f"disciplina {disciplina.code}")

        if not existing.is_custom:
            raise ForbiddenAction(message="catalog disciplina")

        updated = self.repository.update_disciplina(disciplina)
        if updated is None:
            raise NoItemsFound(message=f"disciplina {disciplina.code}")
        return updated
