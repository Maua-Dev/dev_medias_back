import pytest

from src.modules.grade_optmizer.app.genetic_algorithm_usecase import GeneticAlgorithmUsecase
from src.shared.helpers.errors.domain_errors import EntityParameterError, EntityError
from src.shared.helpers.errors.function_errors import FunctionInputError
from src.shared.helpers.errors.usecase_errors import CombinationNotFound, InvalidInput
# Removi dependências antigas que já não são chamadas como a Entidade Nota.

class TestGeneticAlgorithmUsecase:

    def test_possible_grade_usecase(self):
        current_tests = [6.0]
        current_assignments = [6.0, 6.0]
        
        num_remaining_tests = 3
        num_remaining_assignments = 2

        spec_test_weight = [0.2, 0.2, 0.3, 0.3]
        spec_assignment_weight = [0.2, 0.2, 0.3, 0.3]

        test_weight = 0.6
        assignment_weight = 0.4
        media_desejada = 6.0

        usecase = GeneticAlgorithmUsecase()

        for _ in range(3):
            boletim_resp = usecase(
                current_tests=current_tests, current_assignments=current_assignments,
                num_remaining_tests=num_remaining_tests, num_remaining_assignments=num_remaining_assignments,
                test_weight=test_weight, assignment_weight=assignment_weight, target_average=media_desejada,
                spec_test_weight=spec_test_weight, spec_assignment_weight=spec_assignment_weight
            )
            assert abs(round(boletim_resp.final_avg - media_desejada, 2)) <= 0.5

    def test_possible_grade_usecase_2(self):
        current_tests = [6.0, 8.0]
        current_assignments = []
        
        num_remaining_tests = 2
        num_remaining_assignments = 0

        spec_test_weight = [0.2, 0.2, 0.3, 0.3]
        spec_assignment_weight = []

        test_weight = 1.0
        assignment_weight = 0.0
        media_desejada = 7.0 

        usecase = GeneticAlgorithmUsecase()

        for _ in range(3):
            boletim_resp = usecase(
                current_tests=current_tests, current_assignments=current_assignments,
                num_remaining_tests=num_remaining_tests, num_remaining_assignments=num_remaining_assignments,
                test_weight=test_weight, assignment_weight=assignment_weight, target_average=media_desejada,
                spec_test_weight=spec_test_weight, spec_assignment_weight=spec_assignment_weight
            )
            assert abs(round(boletim_resp.final_avg - media_desejada, 2)) <= 0.5
            
    def test_possible_grade_usecase_4(self):
        current_tests = [10.0, 10.0]
        current_assignments = []
        
        num_remaining_tests = 2
        num_remaining_assignments = 0

        spec_test_weight = [0.2, 0.2, 0.3, 0.3]
        spec_assignment_weight = []

        test_weight = 1.0
        assignment_weight = 0.0
        media_desejada = 10.0

        usecase = GeneticAlgorithmUsecase()

        for _ in range(2):
            boletim_resp = usecase(
                current_tests=current_tests, current_assignments=current_assignments,
                num_remaining_tests=num_remaining_tests, num_remaining_assignments=num_remaining_assignments,
                test_weight=test_weight, assignment_weight=assignment_weight, target_average=media_desejada,
                spec_test_weight=spec_test_weight, spec_assignment_weight=spec_assignment_weight
            )
            assert boletim_resp.provas[0]["valor"] == 10.0
            assert boletim_resp.provas[1]["valor"] == 10.0
                  
    def test_possible_grade_usecase_impossivel_de_tirar_nota(self):
        current_tests = [0.0, 8.0]
        current_assignments = []
        
        num_remaining_tests = 2
        num_remaining_assignments = 0

        spec_test_weight = [0.2, 0.2, 0.3, 0.3]
        spec_assignment_weight = []

        test_weight = 1.0
        assignment_weight = 0.0
        media_desejada = 10.0
        
        usecase = GeneticAlgorithmUsecase()
        
        with pytest.raises(CombinationNotFound):
            usecase(
                current_tests=current_tests, current_assignments=current_assignments,
                num_remaining_tests=num_remaining_tests, num_remaining_assignments=num_remaining_assignments,
                test_weight=test_weight, assignment_weight=assignment_weight, target_average=media_desejada,
                spec_test_weight=spec_test_weight, spec_assignment_weight=spec_assignment_weight, generations=50
            )

    def test_possible_grade_usecase_media_desejada_menor_que_minimo_valor(self):
        usecase = GeneticAlgorithmUsecase()

        with pytest.raises(EntityError):
            usecase(
                current_tests=[6.0], current_assignments=[6.0, 6.0],
                num_remaining_tests=3, num_remaining_assignments=2,
                test_weight=0.6, assignment_weight=0.4, target_average=-1.0,
                spec_test_weight=[0.2, 0.2, 0.3, 0.3], spec_assignment_weight=[0.2, 0.2, 0.3, 0.3]
            )

    def test_possible_grade_usecase_media_desejada_maior_que_maximo_valor(self):
        usecase = GeneticAlgorithmUsecase()

        with pytest.raises(EntityError):
            usecase(
                current_tests=[6.0], current_assignments=[6.0, 6.0],
                num_remaining_tests=3, num_remaining_assignments=2,
                test_weight=0.6, assignment_weight=0.4, target_average=100.0,
                spec_test_weight=[0.2, 0.2, 0.3, 0.3], spec_assignment_weight=[0.2, 0.2, 0.3, 0.3]
            )

    def test_possible_grade_usecase_soma_dos_pesos_nao_e_1(self):
        usecase = GeneticAlgorithmUsecase()

        with pytest.raises(EntityError):
            usecase(
                current_tests=[6.0], current_assignments=[6.0, 6.0],
                num_remaining_tests=3, num_remaining_assignments=2,
                test_weight=0.6, assignment_weight=0.4, target_average=6.0,
                spec_test_weight=[0.2, 0.2, 0.3, 0.4], # A soma aqui não é 1
                spec_assignment_weight=[0.2, 0.2, 0.3, 0.4]
            )