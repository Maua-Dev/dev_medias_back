from src.shared.helpers.disciplina.custom_disciplina_payload import parse_create_disciplina_body
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.usecase_errors import DuplicatedItem, ForbiddenAction, InvalidInput
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import (
    BadRequest,
    Conflict,
    Created,
    Forbidden,
    InternalServerError,
)
from src.shared.helpers.http.device_id import require_device_id

from .create_custom_disciplina_usecase import CreateCustomDisciplinaUsecase
from .create_custom_disciplina_viewmodel import CreateCustomDisciplinaViewmodel


class CreateCustomDisciplinaController:

    def __init__(self, usecase: CreateCustomDisciplinaUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            device_id = require_device_id(request.headers)
            body = request.body if isinstance(request.body, dict) else {}
            disciplina = parse_create_disciplina_body(body, device_id=device_id)
            created = self.usecase(disciplina)
            return Created(CreateCustomDisciplinaViewmodel(created).to_dict())

        except MissingParameters as error:
            return BadRequest(error.message)

        except WrongTypeParameter as error:
            return BadRequest(error.message)

        except InvalidInput as error:
            return BadRequest(error.message)

        except DuplicatedItem as error:
            return Conflict(error.message)

        except ForbiddenAction as error:
            return Forbidden(error.message)

        except Exception as error:
            return InternalServerError(error)
