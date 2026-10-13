from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import InternalServerError, NotFound, OK

from .get_all_cursos_usecase import GetAllCursosUsecase
from .get_all_cursos_viewmodel import GetAllCursosViewmodel


class GetAllCursosController:

    def __init__(self, usecase: GetAllCursosUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            cursos = self.usecase()
            viewmodel = GetAllCursosViewmodel(cursos)
            return OK(viewmodel.to_dict())

        except NoItemsFound as error:
            return NotFound(error)

        except Exception as error:
            return InternalServerError(error)
