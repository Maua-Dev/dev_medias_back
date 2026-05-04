from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, InternalServerError
from .get_all_disciplinas_usecase import GetAllDisciplinasUsecase
from .get_all_disciplinas_viewmodel import GetAllDisciplinasViewmodel
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.http_codes import NotFound

class GetAllDisciplinasController:

    def __init__(self, usecase: GetAllDisciplinasUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            
            #TODO implement user logic from request (requester user)
            
            disciplinas = self.usecase()
            viewmodel = GetAllDisciplinasViewmodel(disciplinas)
            return OK(viewmodel.to_dict())
        
        except NoItemsFound as error:
            return NotFound(error)
            
        except Exception as e:
            return InternalServerError(e)