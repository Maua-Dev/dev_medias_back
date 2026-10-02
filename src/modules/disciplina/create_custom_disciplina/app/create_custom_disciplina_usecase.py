from src.shared.domain.entities.disciplina import Disciplina
from src.shared.domain.repositories.disciplina_repository_interface import IDisciplinaRepository
from src.shared.helpers.errors.usecase_errors import DuplicatedItem


class CreateCustomDisciplinaUsecase:

    def __init__(self, repository: IDisciplinaRepository):
        self.repository = repository

    def __call__(self, disciplina: Disciplina) -> Disciplina:
        existing = self.repository.get_disciplina(disciplina.code)
        if existing is not None:
            raise DuplicatedItem(message="code")

        created = self.repository.create_disciplina(disciplina)
        assert created is not None
        return created
