from typing import List
from src.shared.domain.entities.boletim_ga import Boletim_GA
from typing import Optional
from src.shared.domain.entities.nota import Nota
from src.shared.helpers.errors.function_errors import FunctionInputError
from src.shared.helpers.errors.usecase_errors import CombinationNotFound, InvalidInput
from src.shared.genetic_algorithm_solver import GradeGeneticAlgorithm


class GeneticAlgorithmUsecase:
    def __init__(self):
        pass

    def __call__(self, 
                 current_tests: list[float], 
                 current_assignments: list[float],
                 num_remaining_tests: int, 
                 num_remaining_assignments: int,
                 test_weight: float, 
                 assignment_weight: float, 
                 target_average: float,
                 spec_test_weight: list[float], 
                 spec_assignment_weight: list[float],
                 max_grade: float = 10.0,
                 population_size: int = 150,
                 generations: int = 200
                ) -> dict:
        
        # validação dos pesos feita pelo próprio boletim
        boletim = Boletim_GA(current_tests=current_tests, current_assignments=current_assignments, num_remaining_tests=num_remaining_tests, num_remaining_assignments=num_remaining_assignments, test_weight=test_weight, assignment_weight=assignment_weight, spec_test_weight=spec_test_weight, spec_assignment_weight=spec_assignment_weight, max_grade=max_grade)
        
        ga = GradeGeneticAlgorithm(boletim=boletim, target_average=target_average, max_grade=max_grade, population_size=population_size, generations=generations)
        solution, fitness, final_avg = ga.run()
        

        boletim.calculated_tests = solution['tests']
        boletim.calculated_assignments = solution['assignments']
        boletim.target_avg = target_average
        boletim.final_avg = final_avg

        if(solution == None):
            raise CombinationNotFound()
        return boletim