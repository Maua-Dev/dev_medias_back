from src.shared.domain.entities.disciplina import Disciplina
from src.shared.domain.repositories.disciplina_repository_interface import IDisciplinaRepository
from src.shared.environments import Environments
from src.shared.helpers.errors.usecase_errors import NoItemsFound


class GetAllDisciplinasUsecase:

    def __init__(self, repository: IDisciplinaRepository):
        self.repository = repository

    def __call__(self, device_id: str | None = None) -> list[Disciplina]:
        disciplinas = list(self.repository.get_all_disciplinas())

        if device_id:
            device_repo = Environments.get_disciplina_repo(user_id=device_id)
            for item in device_repo.get_all_disciplinas():
                if not item.is_custom:
                    item = item.model_copy(
                        update={"is_custom": True, "device_id": item.device_id or device_id}
                    )
                disciplinas.append(item)

        if not disciplinas:
            raise NoItemsFound(message="disciplinas")

        return disciplinas
