import traceback
from .genetic_algorithm_usecase import GeneticAlgorithmUsecase
from .genetic_algorithm_viewmodel import GeneticAlgorithmViewmodel
from src.shared.domain.entities.nota import Nota
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError, EntityParameterError
from src.shared.helpers.errors.function_errors import FunctionInputError
from src.shared.helpers.errors.usecase_errors import CombinationNotFound, InvalidInput
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError, NotFound


class GeneticAlgorithmController:

    def __init__(self, usecase: GeneticAlgorithmUsecase):
        self.usecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            # ==========================================
            # VALIDAÇÃO: provas_que_tenho
            # ==========================================
            provas_que_tenho = request.data.get('provas_que_tenho')
            if provas_que_tenho is None:
                raise MissingParameters('provas_que_tenho')
            if not isinstance(provas_que_tenho, list):
                raise WrongTypeParameter(
                    fieldName="provas_que_tenho",
                    fieldTypeExpected="list",
                    fieldTypeReceived=type(provas_que_tenho).__name__
                )
            
            # Validação de cada nota e peso da lista provas_que_tenho
            for nota in provas_que_tenho:
                if not isinstance(nota.get('valor'), (int, float)):
                    raise WrongTypeParameter(
                        fieldName="provas_que_tenho item",
                        fieldTypeExpected="float",
                        fieldTypeReceived=type(nota.get('valor')).__name__
                    )
                if not isinstance(nota.get('peso'), (int, float)):
                    raise WrongTypeParameter(
                        fieldName="provas_que_tenho peso item",
                        fieldTypeExpected="float",
                        fieldTypeReceived=type(nota.get('peso')).__name__
                    )
                if nota['peso'] < 0 or nota['peso'] > 1:
                    raise InvalidInput("provas_que_tenho peso item", "Must be between 0 and 1")
            
            current_tests = [nota['valor'] for nota in provas_que_tenho]
            spec_current_test_weight = [nota['peso'] for nota in provas_que_tenho]

            # ==========================================
            # VALIDAÇÃO: trabalhos_que_tenho
            # ==========================================
            trabalhos_que_tenho = request.data.get('trabalhos_que_tenho')
            if trabalhos_que_tenho is None:
                raise MissingParameters('trabalhos_que_tenho')
            if not isinstance(trabalhos_que_tenho, list):
                raise WrongTypeParameter(
                    fieldName="trabalhos_que_tenho",
                    fieldTypeExpected="list",
                    fieldTypeReceived=type(trabalhos_que_tenho).__name__
                )
            
            # Validação de cada nota e peso da lista trabalhos_que_tenho
            for nota in trabalhos_que_tenho:
                if not isinstance(nota.get('valor'), (int, float)):
                    raise WrongTypeParameter(
                        fieldName="trabalhos_que_tenho item",
                        fieldTypeExpected="float",
                        fieldTypeReceived=type(nota.get('valor')).__name__
                    )
                if not isinstance(nota.get('peso'), (int, float)):
                    raise WrongTypeParameter(
                        fieldName="trabalhos_que_tenho peso item",
                        fieldTypeExpected="float",
                        fieldTypeReceived=type(nota.get('peso')).__name__
                    )
                if nota['peso'] < 0 or nota['peso'] > 1:
                    raise InvalidInput("trabalhos_que_tenho peso item", "Must be between 0 and 1")
                
            current_assignments = [nota['valor'] for nota in trabalhos_que_tenho]
            spec_current_assignment_weight = [nota['peso'] for nota in trabalhos_que_tenho]

            # ==========================================
            # VALIDAÇÃO: provas_que_quero
            # ==========================================
            provas_que_quero = request.data.get('provas_que_quero')
            if provas_que_quero is None:
                raise MissingParameters('provas_que_quero')
            if not isinstance(provas_que_quero, list):
                raise WrongTypeParameter(
                    fieldName="provas_que_quero",
                    fieldTypeExpected="list",
                    fieldTypeReceived=type(provas_que_quero).__name__
                )
            
            # Validação de cada peso da lista provas_que_quero
            for nota in provas_que_quero:
                if not isinstance(nota.get('peso'), (int, float)):
                    raise WrongTypeParameter(
                        fieldName="provas_que_quero peso item",
                        fieldTypeExpected="float",
                        fieldTypeReceived=type(nota.get('peso')).__name__
                    )
                if nota['peso'] < 0 or nota['peso'] > 1:
                    raise InvalidInput("provas_que_quero peso item", "Must be between 0 and 1")

            num_remaining_tests = len(provas_que_quero)
            spec_remaining_test_weight = [nota['peso'] for nota in provas_que_quero]

            # ==========================================
            # VALIDAÇÃO: trabalhos_que_quero
            # ==========================================
            trabalhos_que_quero = request.data.get('trabalhos_que_quero')
            if trabalhos_que_quero is None:
                raise MissingParameters('trabalhos_que_quero')
            if not isinstance(trabalhos_que_quero, list):
                raise WrongTypeParameter(
                    fieldName="trabalhos_que_quero",
                    fieldTypeExpected="list",
                    fieldTypeReceived=type(trabalhos_que_quero).__name__
                )
            
            # Validação de cada peso da lista trabalhos_que_quero
            for nota in trabalhos_que_quero:
                if not isinstance(nota.get('peso'), (int, float)):
                    raise WrongTypeParameter(
                        fieldName="trabalhos_que_quero peso item",
                        fieldTypeExpected="float",
                        fieldTypeReceived=type(nota.get('peso')).__name__
                    )
                if nota['peso'] < 0 or nota['peso'] > 1:
                    raise InvalidInput("trabalhos_que_quero peso item", "Must be between 0 and 1")

            num_remaining_assignments = len(trabalhos_que_quero)
            spec_remaining_assignment_weight = [nota['peso'] for nota in trabalhos_que_quero]

            # ==========================================
            # VALIDAÇÃO: pesos gerais e média
            # ==========================================
            peso_prova = request.data.get('peso_prova')
            if peso_prova is None:
                raise MissingParameters('peso_prova')
            if not isinstance(peso_prova, (int, float)):
                raise WrongTypeParameter(
                    fieldName="peso_prova",
                    fieldTypeExpected="float",
                    fieldTypeReceived=type(peso_prova).__name__
                )
            if peso_prova < 0 or peso_prova > 1:
                raise InvalidInput("peso_prova", "Must be between 0 and 1")
            
            peso_trabalho = request.data.get('peso_trabalho')
            if peso_trabalho is None:
                raise MissingParameters('peso_trabalho')
            if not isinstance(peso_trabalho, (int, float)):
                raise WrongTypeParameter(
                    fieldName="peso_trabalho",
                    fieldTypeExpected="float",
                    fieldTypeReceived=type(peso_trabalho).__name__
                )
            if peso_trabalho < 0 or peso_trabalho > 1:
                raise InvalidInput("peso_trabalho", "Must be between 0 and 1")

            media_desejada = request.data.get('media_desejada')
            if media_desejada is None:
                raise MissingParameters('media_desejada')
            if not isinstance(media_desejada, (int, float)):
                raise WrongTypeParameter(
                    fieldName="media_desejada",
                    fieldTypeExpected="float",
                    fieldTypeReceived=type(media_desejada).__name__
                )
            if media_desejada < 0 or media_desejada > 10:
                raise InvalidInput("media_desejada", "Must be between 0 and 10")
            
            if peso_prova + peso_trabalho != 1.0:
                raise InvalidInput("peso_prova and/or peso_trabalho", "Must sum 1.0")

            # ==========================================
            # EXECUÇÃO DO USECASE
            # ==========================================
            spec_assignment_weight = spec_current_assignment_weight + spec_remaining_assignment_weight
            spec_test_weight = spec_current_test_weight + spec_remaining_test_weight

            combinacao_de_notas = self.usecase(
                current_tests=current_tests,
                current_assignments=current_assignments,
                num_remaining_tests=num_remaining_tests,
                num_remaining_assignments=num_remaining_assignments,
                test_weight=peso_prova,
                assignment_weight=peso_trabalho,
                target_average=media_desejada,
                max_grade=10.0,
                population_size=150,
                generations=200,
                spec_test_weight=spec_test_weight,
                spec_assignment_weight=spec_assignment_weight
            )

            viewmodel = GeneticAlgorithmViewmodel(combinacao_de_notas)
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
            return InternalServerError(body=str(err.args[0]) if err.args else "Internal Server Error")