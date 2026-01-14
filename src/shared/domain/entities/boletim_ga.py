from src.shared.helpers.errors.domain_errors import EntityError
from typing import Optional
class Boletim_ga:
    current_tests: list[float] 
    current_assignments: list[float]
    num_remaining_tests: int 
    num_remaining_assignments: int
    test_weight: float
    assignment_weight: float
    spec_test_weight: Optional[list[float]]
    spec_assignment_weight: Optional[list[float]]
    response : dict


    def __init__(self, current_tests: list[float], current_assignments: list[float],
                 num_remaining_tests: int, num_remaining_assignments: int,
                 test_weight: float, assignment_weight: float, spec_test_weight: Optional[list[float]], spec_assignment_weight: Optional[list[float]]):
        
        if type(current_tests) == list:
            if not all(type(item) == float for item in current_tests):
                raise EntityError("current_tests")
            else:
                self.current_tests = current_tests
        else: 
            raise EntityError("current_tests")
        if type(current_assignments) == list:
                    if not all(type(item) == float for item in current_assignments):
                        raise EntityError("current_assignments")
                    else:
                        self.current_assignments = current_assignments
        else: 
            raise EntityError("current_assignments")


        if type(spec_test_weight) == list:
                    if not all(type(item) == float for item in spec_test_weight):
                        raise EntityError("spec_test_weight")
                    else:
                        self.spec_test_weight = spec_test_weight
        else: 
            raise EntityError("spec_test_weight")


        if type(spec_assignment_weight) == list:
                    if not all(type(item) == float for item in spec_assignment_weight):
                        raise EntityError("spec_assignment_weight")
                    else:
                        self.spec_assignment_weight = spec_assignment_weight
        else: 
            raise EntityError("spec_assignment_weight")
        
        if not self.validate_num_remaining_tests(num_remaining_tests):
            raise EntityError("num_remaining_tests")
        self.num_remaining_tests = num_remaining_tests


        if not self.validate_num_remaining_assignments(num_remaining_assignments):
            raise EntityError("num_remaining_assignments")
        self.num_remaining_assignments = num_remaining_assignments


        if not self.validate_test_weight(test_weight):
            raise EntityError("test_weight")
        self.test_weight = test_weight


        if not self.validate_assignment_weight(assignment_weight):
            raise EntityError("assignment_weight")
        self.assignment_weight = assignment_weight


        


    @staticmethod
    def validate_num_remaining_tests(num_remaining_tests: int) -> bool:
        if type(num_remaining_tests) is not int:
            return False
        if num_remaining_tests < 0:
            return False
        return True 

    @staticmethod
    def validate_num_remaining_assignments(num_remaining_assignments: int) -> bool:
            if type(num_remaining_assignments) is not int:
                return False
            if num_remaining_assignments < 0:
                return False
            return True 

    @staticmethod
    def validate_test_weight(test_weight: float) -> bool:
        if type(test_weight) == float:
                if test_weight >= 0:
                    return True
                else:
                    return False
        else:
                return False

    @staticmethod
    def validate_assignment_weight(assignment_weight: float) -> bool:
        if type(assignment_weight) == float:
                if assignment_weight >= 0:
                        return True
                else:
                        return False
        else:
                return False
