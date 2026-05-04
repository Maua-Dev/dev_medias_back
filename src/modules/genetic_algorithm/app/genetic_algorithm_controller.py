import traceback
from .genetic_algorithm_usecase import GeneticAlgorithmUsecase
from .genetic_algorithm_viewmodel import GeneticAlgorithmViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError, EntityParameterError
from src.shared.helpers.errors.function_errors import FunctionInputError
from src.shared.helpers.errors.usecase_errors import CombinationNotFound, InvalidInput
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError, NotFound


class GeneticAlgorithmController:

    def __init__(self, usecase: GeneticAlgorithmUsecase):
        self.usecase = usecase

    def _validate_and_extract_list(self, request_data: dict, field_name: str, check_valor: bool = True) -> tuple[list, list]:
        """
        Valida a lista recebida no payload e extrai os valores e pesos.
        Retorna uma tupla: (lista_de_valores, lista_de_pesos)
        """
        items = request_data.get(field_name)
        if items is None:
            raise MissingParameters(field_name)
        if not isinstance(items, list):
            raise WrongTypeParameter(
                fieldName=field_name,
                fieldTypeExpected="list",
                fieldTypeReceived=type(items).__name__
            )

        valores = []
        pesos = []

        for item in items:
            # Validação do peso (comum a todas as listas)
            peso = item.get('peso')
            if not isinstance(peso, (int, float)):
                raise WrongTypeParameter(
                    fieldName=f"{field_name} peso item",
                    fieldTypeExpected="float",
                    fieldTypeReceived=type(peso).__name__
                )
            if peso < 0 or peso > 1:
                raise InvalidInput(f"{field_name} peso item", "Must be between 0 and 1")
            
            pesos.append(peso)

            # Validação do valor (apenas para as notas que já tenho)
            if check_valor:
                valor = item.get('valor')
                if not isinstance(valor, (int, float)):
                    raise WrongTypeParameter(
                        fieldName=f"{field_name} item",
                        fieldTypeExpected="float",
                        fieldTypeReceived=type(valor).__name__
                    )
                valores.append(valor)

        return valores, pesos

    def __call__(self, request: IRequest) -> IResponse:
        try:
            # ==========================================
            # VALIDAÇÃO: Extração limpa usando o método auxiliar
            # ==========================================
            current_tests, spec_current_test_weight = self._validate_and_extract_list(
                request.data, 'provas_que_tenho', check_valor=True
            )
            
            current_assignments, spec_current_assignment_weight = self._validate_and_extract_list(
                request.data, 'trabalhos_que_tenho', check_valor=True
            )
            
            _, spec_remaining_test_weight = self._validate_and_extract_list(
                request.data, 'provas_que_quero', check_valor=False
            )
            num_remaining_tests = len(spec_remaining_test_weight)
            
            _, spec_remaining_assignment_weight = self._validate_and_extract_list(
                request.data, 'trabalhos_que_quero', check_valor=False
            )
            num_remaining_assignments = len(spec_remaining_assignment_weight)

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
            
            if abs((peso_prova + peso_trabalho) - 1.0) > 0.01: # Uso de tolerância de float
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

        # ... (seus blocos except continuam exatamente os mesmos) ...
        except InvalidInput as err:
            return BadRequest(body=err.message)
        # ...