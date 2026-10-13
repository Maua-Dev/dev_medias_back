from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.usecase_errors import DuplicatedItem
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import BadRequest, Conflict, Created, InternalServerError

from .create_curso_usecase import CreateCursoUsecase
from .create_curso_viewmodel import CreateCursoViewmodel


class CreateCursoController:

    def __init__(self, usecase: CreateCursoUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('código') is None:
                raise MissingParameters('código')
            if type(request.data.get('código')) != str:
                raise WrongTypeParameter(
                    fieldName='código',
                    fieldTypeExpected='str',
                    fieldTypeReceived=request.data.get('código').__class__.__name__,
                )

            if request.data.get('nome') is None:
                raise MissingParameters('nome')
            if type(request.data.get('nome')) != str:
                raise WrongTypeParameter(
                    fieldName='nome',
                    fieldTypeExpected='str',
                    fieldTypeReceived=request.data.get('nome').__class__.__name__,
                )

            curso = self.usecase(
                código=request.data.get('código'),
                nome=request.data.get('nome'),
            )
            viewmodel = CreateCursoViewmodel(curso)

            return Created(viewmodel.to_dict())

        except MissingParameters as error:
            return BadRequest(error.message)

        except WrongTypeParameter as error:
            return BadRequest(error.message)

        except DuplicatedItem as error:
            return Conflict(error.message)

        except Exception as error:
            return InternalServerError(error)
