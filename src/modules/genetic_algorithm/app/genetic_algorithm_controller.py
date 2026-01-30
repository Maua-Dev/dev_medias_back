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
            if request.data.get('current_tests') is None:
                raise MissingParameters('current_tests')
            if type(request.data.get('current_tests')) != list:
                raise WrongTypeParameter(
                    fieldName="current_tests",
                    fieldTypeExpected="list",
                    fieldTypeReceived=request.data.get('current_tests').__class__.__name__
                )
            for nota in request.data.get('current_tests'):
                if not isinstance(nota, (int, float)):
                    raise WrongTypeParameter(
                        fieldName="current_tests item",
                        fieldTypeExpected="float",
                        fieldTypeReceived=nota.__class__.__name__
                    )
                if nota == None:
                    raise WrongTypeParameter(
                        fieldName="current_tests item",
                        fieldTypeExpected="float",
                        fieldTypeReceived=nota.__class__.__name__
                    )

            current_tests = [nota for nota in request.data.get('current_tests')]



            if request.data.get('current_assignments') is None:
                raise MissingParameters('current_assignments')
            if type(request.data.get('current_assignments')) != list:
                raise WrongTypeParameter(
                    fieldName="current_assignments",
                    fieldTypeExpected="list",
                    fieldTypeReceived=request.data.get('current_assignments').__class__.__name__
                )
            for nota in request.data.get('current_assignments'):
                if not isinstance(nota, (int, float)):
                    raise WrongTypeParameter(
                        fieldName="current_tests item",
                        fieldTypeExpected="float",
                        fieldTypeReceived=nota.__class__.__name__
                    )
            current_assignments = [nota for nota in request.data.get('current_assignments')]


                
            if request.data.get('num_remaining_tests') is None:
                raise MissingParameters('num_remaining_tests')
            if type(request.data.get('num_remaining_tests')) != int:
                raise WrongTypeParameter(
                    fieldName="num_remaining_tests",
                    fieldTypeExpected="int",
                    fieldTypeReceived=request.data.get('num_remaining_tests').__class__.__name__
                )
            if request.data.get('num_remaining_tests') < 0:
                raise InvalidInput("num_remaining_tests", "Must be non-negative")

            num_remaining_tests = request.data.get('num_remaining_tests')


            if request.data.get('num_remaining_assignments') is None:
                raise MissingParameters('num_remaining_assignments')
            if type(request.data.get('num_remaining_assignments')) != int:
                raise WrongTypeParameter(
                    fieldName="num_remaining_assignments",
                    fieldTypeExpected="int",
                    fieldTypeReceived=request.data.get('num_remaining_assignments').__class__.__name__
                )
            if request.data.get('num_remaining_assignments') < 0:
                raise InvalidInput("num_remaining_assignments", "Must be non-negative")

            num_remaining_assignments = request.data.get('num_remaining_assignments')



            if request.data.get('test_weight') is None:
                raise MissingParameters('test_weight')
            if type(request.data.get('test_weight')) != float:
                raise WrongTypeParameter(
                    fieldName="test_weight",
                    fieldTypeExpected="float",
                    fieldTypeReceived=request.data.get('test_weight').__class__.__name__
                )
            if request.data.get('test_weight') < 0 or request.data.get('test_weight') > 1:
                raise InvalidInput("test_weight", "Must be between 0 and 1")
            
            test_weight = request.data.get('test_weight')




            if request.data.get('assignment_weight') is None:
                raise MissingParameters('assignment_weight')
            if type(request.data.get('assignment_weight')) != float:
                raise WrongTypeParameter(
                    fieldName="assignment_weight",
                    fieldTypeExpected="float",
                    fieldTypeReceived=request.data.get('assignment_weight').__class__.__name__
                )
            if request.data.get('assignment_weight') < 0 or request.data.get('assignment_weight') > 1:
                raise InvalidInput("assignment_weight", "Must be between 0 and 1")
            
            assignment_weight = request.data.get('assignment_weight')


            if request.data.get('target_average') is None:
                raise MissingParameters('target_average')
            if type(request.data.get('target_average')) != float:
                raise WrongTypeParameter(
                    fieldName="target_average",
                    fieldTypeExpected="float",
                    fieldTypeReceived=request.data.get('target_average').__class__.__name__
                )
            if request.data.get('target_average') < 0 or request.data.get('target_average') > 10:
                raise InvalidInput("target_average", "Must be between 0 and 10")

            target_average = request.data.get('target_average')

            if request.data.get('max_grade') is not None:
                if type(request.data.get('max_grade')) != float:
                    raise WrongTypeParameter(
                        fieldName="max_grade",
                        fieldTypeExpected="float",
                        fieldTypeReceived=request.data.get('max_grade').__class__.__name__
                    )
                if request.data.get('max_grade') <= 0:
                    raise InvalidInput("max_grade", "Must be greater than 0")
                max_grade = request.data.get('max_grade')
            else:
                max_grade = 10.0
            
            if request.data.get('population_size') is not None:
                if type(request.data.get('population_size')) != int:
                    raise WrongTypeParameter(
                        fieldName="population_size",
                        fieldTypeExpected="int",
                        fieldTypeReceived=request.data.get('population_size').__class__.__name__
                    )
                if request.data.get('population_size') <= 0:
                    raise InvalidInput("population_size", "Must be greater than 0")
                population_size = request.data.get('population_size')
            else:
                population_size = 100
            
            if request.data.get('generations') is not None:
                if type(request.data.get('generations')) != int:
                    raise WrongTypeParameter(
                        fieldName="generations",
                        fieldTypeExpected="int",
                        fieldTypeReceived=request.data.get('generations').__class__.__name__
                    )
                if request.data.get('generations') <= 0:
                    raise InvalidInput("generations", "Must be greater than 0")
                generations = request.data.get('generations')
            else:
                generations = 200
            
            if request.data.get('spec_test_weight') is not None:
                if type(request.data.get('spec_test_weight')) != list:
                    raise WrongTypeParameter(
                        fieldName="spec_test_weight",
                        fieldTypeExpected="list",
                        fieldTypeReceived=request.data.get('spec_test_weight').__class__.__name__
                    )
                
                if len(request.data.get('spec_test_weight')) != len(current_tests) + num_remaining_tests:
                    raise InvalidInput("spec_test_weight", "Must have the same length as the sum of current_tests and num_remaining_tests")
                
                for weight in request.data.get('spec_test_weight'):
                    if not isinstance(weight, (int, float)):
                        raise WrongTypeParameter(
                            fieldName="spec_test_weight item",
                            fieldTypeExpected="float",
                            fieldTypeReceived=weight.__class__.__name__
                        )
                    if weight < 0 or weight > 1:
                        raise InvalidInput("spec_test_weight", "All values must be between 0 and 1")
                if abs(sum(request.data.get('spec_test_weight')) - 1.0) > 0.01:
                    raise InvalidInput("spec_test_weight", "The sum must be equal to 1")
                spec_test_weight = request.data.get('spec_test_weight')
            else:
                spec_test_weight = None
            
            if request.data.get('spec_assignment_weight') is not None:
                if type(request.data.get('spec_assignment_weight')) != list:
                    raise WrongTypeParameter(
                        fieldName="spec_assignment_weight",
                        fieldTypeExpected="list",
                        fieldTypeReceived=request.data.get('spec_assignment_weight').__class__.__name__
                    )

                if len(request.data.get('spec_assignment_weight')) != len(current_assignments) + num_remaining_assignments:
                    raise InvalidInput("spec_assignment_weight", "Must have the same length as the sum of current_assignments and num_remaining_assignments")

                for weight in request.data.get('spec_assignment_weight'):
                    if not isinstance(weight, (int, float)):
                        raise WrongTypeParameter(
                            fieldName="spec_assignment_weight item",
                            fieldTypeExpected="float",
                            fieldTypeReceived=weight.__class__.__name__
                        )
                    if weight < 0 or weight > 1:
                        raise InvalidInput("spec_assignment_weight", "All values must be between 0 and 1")
                if abs(sum(request.data.get('spec_assignment_weight')) - 1.0) > 0.01:
                    raise InvalidInput("spec_assignment_weight", "The sum must be equal to 1")
                spec_assignment_weight = request.data.get('spec_assignment_weight')
            else:
                spec_assignment_weight = None

            combinacao_de_notas = self.usecase(
                current_tests=current_tests,
                current_assignments=current_assignments,
                num_remaining_tests=num_remaining_tests,
                num_remaining_assignments=num_remaining_assignments,
                test_weight=test_weight,
                assignment_weight=assignment_weight,
                target_average=target_average,
                max_grade=max_grade,
                population_size=population_size,
                generations=generations,
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
            return InternalServerError(body=err.args[0])