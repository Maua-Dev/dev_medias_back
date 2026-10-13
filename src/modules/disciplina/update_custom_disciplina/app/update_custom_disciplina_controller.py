from src.shared.helpers.disciplina.custom_disciplina_payload import (
    parse_update_disciplina_body,
    resolve_code_from_request,
)
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

from .update_custom_disciplina_usecase import UpdateCustomDisciplinaUsecase
from .update_custom_disciplina_viewmodel import UpdateCustomDisciplinaViewmodel


class UpdateCustomDisciplinaController:

    def __init__(self, usecase: UpdateCustomDisciplinaUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            device_id = require_device_id(request.headers)
            body = request.body if isinstance(request.body, dict) else {}
            code = resolve_code_from_request(body, getattr(request, "query_params", None))

            existing = self.usecase.repository.get_disciplina(code)
            if existing is None:
                raise NoItemsFound(message=f"disciplina {code}")

            disciplina = parse_update_disciplina_body(
                body,
                existing=existing,
                device_id=device_id,
            )
            updated = self.usecase(disciplina)
            return OK(UpdateCustomDisciplinaViewmodel(updated).to_dict())

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
