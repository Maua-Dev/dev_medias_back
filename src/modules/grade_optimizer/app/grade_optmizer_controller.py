from src.modules.grade_optimizer.app import grade_optmizer_usecase
from src.modules.grade_optimizer.app.grade_optmizer_viewmodel import GradeOptmizerViewmodel
from src.shared.domain.entities.nota import Nota
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError


class GradeOptmizerController:

    def __init__(self, usecase: grade_optmizer_usecase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            if request.data.get('notas_que_tenho') is None:
                raise MissingParameters('notas_que_tenho')
            if type(request.data.get('notas_que_tenho')) != list:
                raise WrongTypeParameter(
                    fieldName="notas_que_tenho",
                    fieldTypeExpected="list",
                    fieldTypeReceived=request.data.get('user_id').__class__.__name__
                )
            for nota in request.data.get('notas_que_tenho'):
                if(type(nota) != dict):
                    raise EntityError("notas_que_tenho")
                if(nota.get('valor') == None or type(nota.get('valor')) != float):
                    raise EntityError("valor")
                if(nota.get('peso') == None or type(nota.get('peso')) != float):
                    raise EntityError("peso")
            notas_que_tenho = [Nota(valor=nota["valor"], peso=nota["peso"]) for nota in request.data.get('notas_que_tenho')]
                
            if request.data.get('notas_que_quero') is None:
                raise MissingParameters('notas_que_quero')
            if type(request.data.get('notas_que_quero')) != list:
                raise WrongTypeParameter(
                    fieldName="notas_que_quero",
                    fieldTypeExpected="list",
                    fieldTypeReceived=request.data.get('user_id').__class__.__name__
                )
            for nota in request.data.get('notas_que_quero'):
                if(type(nota) != dict):
                    raise EntityError("notas_que_quero")
                if(nota.get('peso') == None or type(nota.get('peso')) != float):
                    raise EntityError("peso")
                if(nota.get('valor') != None):
                    raise EntityError("valor")
            notas_que_quero = [Nota(valor=nota["valor"], peso=nota["peso"]) for nota in request.data.get('notas_que_quero')]    
            
            if type(request.data.get('media_desejada')) != float:
                raise WrongTypeParameter(
                    fieldName="media_desejada",
                    fieldTypeExpected="float",
                    fieldTypeReceived=request.data.get('media_desejada').__class__.__name__
                )
                

            combinacao_de_notas = self.usecase(
                notas_que_tenho=notas_que_tenho,
                notas_que_quero=notas_que_quero,
                media_desejada=request.data.get('media_desejada')
            )

            viewmodel = GradeOptmizerViewmodel(combinacao_de_notas)

            return OK(viewmodel.to_dict())

        except MissingParameters as err:

            return BadRequest(body=err.message)

        except WrongTypeParameter as err:

            return BadRequest(body=err.message)

        except EntityError as err:

            return BadRequest(body=err.message)

        except Exception as err:

            return InternalServerError(body=err.args[0])
