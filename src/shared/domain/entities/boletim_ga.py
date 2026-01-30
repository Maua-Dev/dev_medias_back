from src.shared.helpers.errors.domain_errors import EntityError, EntityParameterError
from typing import Optional

class Boletim_GA:
    current_tests: list[float] 
    current_assignments: list[float]
    num_remaining_tests: int 
    num_remaining_assignments: int
    test_weight: float
    assignment_weight: float
    spec_test_weight: Optional[list[float]] 
    spec_assignment_weight: Optional[list[float]]
    response: dict
    target_avg: float 
    max_grade: float 

    def __init__(
        self, 
        current_tests: list[float], 
        current_assignments: list[float],
        num_remaining_tests: int, 
        num_remaining_assignments: int,
        test_weight: float, 
        assignment_weight: float, 
        spec_test_weight: Optional[list[float]] = None, 
        spec_assignment_weight: Optional[list[float]] = None,
        max_grade: float = 10.0
    ):
        # Valida e atribui num_remaining
        if not self.validate_num_remaining(num_remaining_tests):
            raise EntityError("num_remaining_tests")
        self.num_remaining_tests = num_remaining_tests

        if not self.validate_num_remaining(num_remaining_assignments):
            raise EntityError("num_remaining_assignments")
        self.num_remaining_assignments = num_remaining_assignments

        # Valida e atribui pesos gerais
        if not self.validate_sum_weights(test_weight, assignment_weight):
            raise EntityError("test_weight and/or assignment_weight (devem somar 1.0)")
        
        if not self.validate_weights(test_weight):
            raise EntityError("test_weight")
        self.test_weight = test_weight

        if not self.validate_weights(assignment_weight):
            raise EntityError("assignment_weight")
        self.assignment_weight = assignment_weight

        # Valida e atribui listas de notas
        if not self.validate_tests(current_tests, max_grade):
            raise EntityError("current_tests")
        self.current_tests = current_tests

        if not self.validate_tests(current_assignments, max_grade):
            raise EntityError("current_assignments")
        self.current_assignments = current_assignments

        
        if spec_test_weight is not None:
            if not self.validate_sum_spec_weights(spec_test_weight, current_tests, num_remaining_tests):
                raise EntityError("spec_test_weight")
            if not self.validate_spec_weights(spec_test_weight):
                raise EntityError("spec_test_weight")
        self.spec_test_weight = spec_test_weight

        if spec_assignment_weight is not None:
            if not self.validate_sum_spec_weights(spec_assignment_weight, current_assignments, num_remaining_assignments):
                raise EntityError("spec_assignment_weight")
            if not self.validate_spec_weights(spec_assignment_weight):
                raise EntityError("spec_assignment_weight")
        self.spec_assignment_weight = spec_assignment_weight

       
        self.response = self.to_dict()

    @staticmethod
    def validate_num_remaining(num_remaining: int) -> bool:
        if not isinstance(num_remaining, int):
            return False
        if num_remaining < 0:
            return False
        return True 

    @staticmethod
    def validate_weights(weight: float) -> bool:
        if not isinstance(weight, (float, int)):
            return False
        if not (0 <= weight <= 1):
            return False
        return True

    @staticmethod
    def validate_tests(current_tests: list[float], max_grade: float) -> bool:
        if not isinstance(current_tests, list):
            return False
        if not all(isinstance(item, (float, int)) for item in current_tests):
            return False
        for test in current_tests:
            if test % 0.5 != 0:
                return False
            if test < 0 or test > max_grade:
                return False
        return True
        
    @staticmethod
    def validate_spec_weights(spec_weight: list[float]) -> bool:
        if not isinstance(spec_weight, list):
            return False
        if not all(isinstance(item, (float, int)) for item in spec_weight):
            return False
        for weight in spec_weight:
            if not (0 <= weight <= 1):
                return False
        return True

    @staticmethod
    def validate_sum_weights(weight1: float, weight2: float) -> bool:
        return abs((weight1 + weight2) - 1.0) < 0.01  # Tolerância para float

    @staticmethod
    def validate_sum_spec_weights(
        spec_weight: list[float], 
        current_tests: list[float], 
        num_remaining_tests: int
    ) -> bool:
        if spec_weight is None:
            return True
        if len(spec_weight) != len(current_tests) + num_remaining_tests:
            return False
        if abs(sum(spec_weight) - 1.0) > 0.01:
            return False
        return True

    def to_dict(self) -> dict:
        """Converte o boletim para dicionário."""
        return {
            "current_tests": self.current_tests,
            "current_assignments": self.current_assignments,
            "num_remaining_tests": self.num_remaining_tests,
            "num_remaining_assignments": self.num_remaining_assignments,
            "test_weight": self.test_weight,
            "assignment_weight": self.assignment_weight,
            "spec_test_weight": self.spec_test_weight,
            "spec_assignment_weight": self.spec_assignment_weight
        }