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
                 max_grade: float = 10.0,
                 population_size: int = 150,
                 generations: int = 200, 
                 spec_test_weight: Optional[list[float]] = None, 
                 spec_assignment_weight: Optional[list[float]] = None
                ) -> dict:
        
        #Validações das variáveis de entrada
        
        if type(max_grade) != float:
            raise InvalidInput("max_grade", "Deve ser um valor do tipo float")
        if max_grade <= 0:
            raise InvalidInput("max_grade", "Deve ser um valor maior que 0")
        
        if type(target_average) != float:
            raise InvalidInput("target_average", "Deve ser um valor do tipo float")
        if target_average < 0 or target_average > max_grade:
            raise InvalidInput("target_average", f"Deve estar entre 0 e {max_grade}")
        
        if test_weight + assignment_weight != 1.0:
            raise InvalidInput("test_weight and/or assignment_weight", "Devem somar 1.0")
        
        # validação dos pesos feita pelo próprio boletim
        boletim = Boletim_GA(current_tests=current_tests, current_assignments=current_assignments, num_remaining_tests=num_remaining_tests, num_remaining_assignments=num_remaining_assignments, test_weight=test_weight, assignment_weight=assignment_weight, spec_test_weight=spec_test_weight, spec_assignment_weight=spec_assignment_weight, max_grade=max_grade)
        
        ga = GradeGeneticAlgorithm(boletim=boletim, target_average=target_average, max_grade=max_grade, population_size=population_size, generations=generations)
        solution, fitness = ga.run()
        response = {
            "current_tests": current_tests,
            "current_assignments": current_assignments,
            "tests": solution['tests'],
            "assignments": solution['assignments'],
            "test_weight": test_weight,
            "assignment_weight": assignment_weight,
            "spec_test_weight": spec_test_weight,
            "spec_assignment_weight": spec_assignment_weight,
            "num_remaining_tests": num_remaining_tests,
            "num_remaining_assignments": num_remaining_assignments,
            "target_average": target_average
        }

        boletim.calculated_tests = solution['tests']
        boletim.calculated_assignments = solution['assignments']
        boletim.target_avg = target_average

        if(response == None):
            raise CombinationNotFound()
        return response