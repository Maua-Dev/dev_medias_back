from src.shared.domain.entities.disciplina import Disciplina
from src.shared.domain.repositories.disciplina_repository_interface import IDisciplinaRepository
from src.shared.helpers.errors.usecase_errors import NoItemsFound

class GetAllDisciplinasUsecase:
    
    def __init__(self, repository: IDisciplinaRepository):
        self.repository = repository

    #TODO implement user logic from request (requester user)

    def __call__(self) -> list[Disciplina]:
        
        disciplinas = self.repository.get_all_disciplinas()
        
        if not disciplinas:
            
            raise NoItemsFound(message='disciplinas')
        
        return disciplinas