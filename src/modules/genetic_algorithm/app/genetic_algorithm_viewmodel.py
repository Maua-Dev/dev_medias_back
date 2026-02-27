from urllib import response

from src.shared.domain.entities import boletim
from src.shared.domain.entities.boletim_ga import Boletim_GA
from src.shared.domain.entities.nota import Nota



class GeneticAlgorithmViewmodel:
    

    def __init__(self, boletim: Boletim_GA):
        self.boletim = boletim

    def to_dict(self) -> dict:
        response = {
            "current_tests": self.boletim.current_tests,
            "current_assignments": self.boletim.current_assignments,
            "tests": self.boletim.calculated_tests,
            "assignments": self.boletim.calculated_assignments,
            "test_weight": self.boletim.test_weight,
            "assignment_weight": self.boletim.assignment_weight,
            "spec_test_weight": self.boletim.spec_test_weight,
            "spec_assignment_weight": self.boletim.spec_assignment_weight,
            "num_remaining_tests": self.boletim.num_remaining_tests,
            "num_remaining_assignments": self.boletim.num_remaining_assignments,
            "target_average": self.boletim.target_avg,
            "final_average": self.boletim.final_avg,
            "calculated_tests": self.boletim.calculated_tests,
            "calculated_assignments": self.boletim.calculated_assignments
        }
    
        return response
    
