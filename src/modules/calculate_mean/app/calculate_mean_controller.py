import traceback
from .calculate_mean_usecase import CalculateMeanUsecase
from .calculate_mean_viewmodel import CalculateMeanViewmodel
from src.shared.domain.entities.nota import Nota
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError, EntityParameterError
from src.shared.helpers.errors.function_errors import FunctionInputError
from src.shared.helpers.errors.usecase_errors import CombinationNotFound, InvalidInput
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError, NotFound


class CalculateMeanController:

    def __init__(self, usecase: CalculateMeanUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('provas_que_tenho') is None:
                raise MissingParameters('provas_que_tenho')
            if type(request.data.get('provas_que_tenho')) != list:
                raise WrongTypeParameter(
                    fieldName="provas_que_tenho",
                    fieldTypeExpected="list",
                    fieldTypeReceived=request.data.get('provas_que_tenho').__class__.__name__
                )
            for nota in request.data.get('provas_que_tenho'):
                if(type(nota) != dict):
                    raise EntityError("provas_que_tenho")
                if(nota.get('valor') == None):
                    raise EntityError("valor")
                if(nota.get('peso') == None):
                    raise EntityError("peso")
            provas_que_tenho = [Nota(valor=nota.get('valor'), peso=nota.get('peso')) for nota in request.data.get('provas_que_tenho')]
                
            if request.data.get('trabalhos_que_tenho') is None:
                raise MissingParameters('trabalhos_que_tenho')
            if type(request.data.get('trabalhos_que_tenho')) != list:
                raise WrongTypeParameter(
                    fieldName="trabalhos_que_tenho",
                    fieldTypeExpected="list",
                    fieldTypeReceived=request.data.get('trabalhos_que_tenho').__class__.__name__
                )
            for nota in request.data.get('trabalhos_que_tenho'):
                if(type(nota) != dict):
                    raise EntityError("trabalhos_que_tenho")
                if(nota.get('valor') == None):
                    raise EntityError("valor")
                if(nota.get('peso') == None):
                    raise EntityError("peso")
            trabalhos_que_tenho = [Nota(valor=nota.get('valor'), peso=nota.get('peso')) for nota in request.data.get('trabalhos_que_tenho')]
                
                
            combinacao_de_notas = self.usecase(
                provas_que_tenho=provas_que_tenho,
                trabalhos_que_tenho=trabalhos_que_tenho,
                peso_prova=request.data.get('peso_prova'),
                peso_trabalho=request.data.get('peso_trabalho')
            )

            viewmodel = CalculateMeanViewmodel(combinacao_de_notas)

            return OK(viewmodel.to_dict())

        except InvalidInput as err:
            return BadRequest(body=err.message)
        
        except CombinationNotFound as err:
            return NotFound(body=err.message)
        
        except EntityParameterError as err:
            return BadRequest(body=err.message)

        except FunctionInputError as err:
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            return BadRequest(body=err.message)
        
        except MissingParameters as err:
            return BadRequest(body=err.message)

        except EntityError as err:
            return BadRequest(body=err.message)

        except Exception as err:
            traceback.print_exc()
            return InternalServerError(body=err.args[0])
