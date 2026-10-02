from src.shared.domain.entities.disciplina import Disciplina
from src.shared.domain.repositories.disciplina_repository_interface import IDisciplinaRepository
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, ForbiddenAction

MAX_CUSTOM_DISCIPLINAS_PER_DEVICE = 20


class CreateCustomDisciplinaUsecase:

    def __init__(self, repository: IDisciplinaRepository):
        self.repository = repository

    def __call__(self, disciplina: Disciplina) -> Disciplina:
        existing = self.repository.get_disciplina(disciplina.code)
        if existing is not None:
            raise DuplicatedItem(message="code")

        current_count = len(self.repository.get_all_disciplinas())
        if current_count >= MAX_CUSTOM_DISCIPLINAS_PER_DEVICE:
            raise ForbiddenAction(
                message=f"custom disciplina limit (max {MAX_CUSTOM_DISCIPLINAS_PER_DEVICE} per device)"
            )

        created = self.repository.create_disciplina(disciplina)
        assert created is not None
        return created
