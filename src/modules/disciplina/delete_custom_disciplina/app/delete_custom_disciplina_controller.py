from src.shared.helpers.disciplina.custom_disciplina_payload import resolve_code_from_request
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, InvalidInput, NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import (
    BadRequest,
    Forbidden,
    InternalServerError,
    NotFound,
    OK,
)
from src.shared.helpers.http.device_id import require_device_id

from .delete_custom_disciplina_usecase import DeleteCustomDisciplinaUsecase
from .delete_custom_disciplina_viewmodel import DeleteCustomDisciplinaViewmodel


class DeleteCustomDisciplinaController:

    def __init__(self, usecase: DeleteCustomDisciplinaUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            require_device_id(request.headers)
            body = request.body if isinstance(request.body, dict) else {}
            code = resolve_code_from_request(body, getattr(request, "query_params", None))
            removed = self.usecase(code)
            return OK(DeleteCustomDisciplinaViewmodel(removed).to_dict())

        except MissingParameters as error:
            return BadRequest(error.message)

        except WrongTypeParameter as error:
            return BadRequest(error.message)

        except InvalidInput as error:
            return BadRequest(error.message)

        except ForbiddenAction as error:
            return Forbidden(error.message)

        except NoItemsFound as error:
            return NotFound(error.message)

        except Exception as error:
            return InternalServerError(error)
