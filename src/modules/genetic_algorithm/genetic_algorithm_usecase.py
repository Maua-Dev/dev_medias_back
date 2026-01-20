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
        if(len(current_tests) < 0 or len(current_assignments) < 0):
            raise InvalidInput("current_tests e current_assignments", "Não podem ser listas vazias")
        
        if type(max_grade) != float:
            raise InvalidInput("max_grade", "Deve ser um valor do tipo float")
        if max_grade <= 0:
            raise InvalidInput("max_grade", "Deve ser um valor maior que 0")
        
        if (test < 0 or test > max_grade for test in current_tests):
            raise InvalidInput("current_tests", f"Todos os valores devem estar entre 0 e {max_grade}")
        if (not all(type(item) == float for item in current_tests)):
            raise InvalidInput("current_tests", "Todos os valores devem ser do tipo float")
        
        if (assignment < 0 or assignment > max_grade for assignment in current_assignments):
            raise InvalidInput("current_assignments", f"Todos os valores devem estar entre 0 e {max_grade}")
        if (not all(type(item) == float for item in current_assignments)):
            raise InvalidInput("current_assignments", "Todos os valores devem ser do tipo float")

        if num_remaining_tests < 0:
            raise InvalidInput("num_remaining_tests", "Deve ser um valor maior ou igual a 0")
        if type(num_remaining_tests) != int:
            raise InvalidInput("num_remaining_tests", "Deve ser um valor do tipo inteiro")
        
        if num_remaining_assignments < 0:
            raise InvalidInput("num_remaining_assignments", "Deve ser um valor maior ou igual a 0")
        if type(num_remaining_assignments) != int:
            raise InvalidInput("num_remaining_assignments", "Deve ser um valor do tipo inteiro")
        
        if type(test_weight) != float:
            raise InvalidInput("test_weight", "Deve ser um valor do tipo float")
        if test_weight < 0 or test_weight > 1:
            raise InvalidInput("test_weight", "Deve estar entre 0 e 1")

        if type(assignment_weight) != float:
            raise InvalidInput("assignment_weight", "Deve ser um valor do tipo float")
        if assignment_weight < 0 or assignment_weight > 1:
            raise InvalidInput("assignment_weight", "Deve estar entre 0 e 1")
        
        if (test_weight + assignment_weight) != 1.0:
            raise InvalidInput("test_weight e assignment_weight", "A soma dos dois deve ser igual a 1")
        
        if type(target_average) != float:
            raise InvalidInput("target_average", "Deve ser um valor do tipo float")
        if target_average < 0 or target_average > max_grade:
            raise InvalidInput("target_average", f"Deve estar entre 0 e {max_grade}")
        
        if type(population_size) != int:
            raise InvalidInput("population_size", "Deve ser um valor do tipo inteiro")
        if population_size <= 0:
            raise InvalidInput("population_size", "Deve ser um valor maior que 0")
        
        if type(generations) != int:
            raise InvalidInput("generations", "Deve ser um valor do tipo inteiro")
        if generations <= 0:
            raise InvalidInput("generations", "Deve ser um valor maior que 0")
        
        if spec_test_weight is not None:
            if len(spec_test_weight) != len(current_tests) + num_remaining_tests:
                raise InvalidInput("spec_test_weight", "Deve ter o mesmo tamanho que a soma de current_tests e num_remaining_tests")
            if (not all(type(item) == float for item in spec_test_weight)):
                raise InvalidInput("spec_test_weight", "Todos os valores devem ser do tipo float")
            if (not all(weight < 0 or weight > 1 for weight in spec_test_weight)):
                raise InvalidInput("spec_test_weight", "Todos os valores devem estar entre 0 e 1")
            if abs(sum(spec_test_weight) - 1.0) > 0.01:
                raise InvalidInput("spec_test_weight", "A soma dos valores deve ser igual a 1")
        
        if spec_assignment_weight is not None:
            if len(spec_assignment_weight) != len(current_assignments) + num_remaining_assignments:
                raise InvalidInput("spec_assignment_weight", "Deve ter o mesmo tamanho que a soma de current_assignments e num_remaining_assignments")
            if (not all(type(item) == float for item in spec_assignment_weight)):
                raise InvalidInput("spec_assignment_weight", "Todos os valores devem ser do tipo float")
            if (not all(weight < 0 or weight > 1 for weight in spec_assignment_weight)):
                raise InvalidInput("spec_assignment_weight", "Todos os valores devem estar entre 0 e 1")
            if abs(sum(spec_assignment_weight) - 1.0) > 0.01:
                raise InvalidInput("spec_assignment_weight", "A soma dos valores deve ser igual a 1")
        
        

        
        # validação dos pesos feita pelo próprio boletim
        boletim = Boletim_GA(current_tests=current_tests, current_assignments=current_assignments, num_remaining_tests=num_remaining_tests, num_remaining_assignments=num_remaining_assignments, test_weight=test_weight, assignment_weight=assignment_weight, spec_test_weight=spec_test_weight, spec_assignment_weight=spec_assignment_weight)
        
        ga = GradeGeneticAlgorithm(boletim=boletim, target_average=target_average, max_grade=max_grade, population_size=population_size, generations=generations)
        solution, fitness = ga.run()
        response = ga.get_results_json(solution=solution)

        if(response == None):
            raise CombinationNotFound()
        return response