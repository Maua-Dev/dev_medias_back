from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.usecase_errors import InvalidInput, NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import (
    BadRequest,
    InternalServerError,
    NotFound,
    OK,
)
from src.shared.helpers.http.device_id import extract_device_id_header, require_device_id

from .get_all_disciplinas_usecase import GetAllDisciplinasUsecase
from .get_all_disciplinas_viewmodel import GetAllDisciplinasViewmodel


class GetAllDisciplinasController:

    def __init__(self, usecase: GetAllDisciplinasUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            device_id = None
            raw_header = extract_device_id_header(request.headers)
            if raw_header is not None:
                # Header present → must be a valid UUID; then merge customs.
                device_id = require_device_id(request.headers)

            disciplinas = self.usecase(device_id=device_id)
            viewmodel = GetAllDisciplinasViewmodel(disciplinas)
            return OK(viewmodel.to_dict())

        except MissingParameters as error:
            return BadRequest(error.message)

        except InvalidInput as error:
            return BadRequest(error.message)

        except NoItemsFound as error:
            return NotFound(error.message)

        except Exception as error:
            return InternalServerError(error)
