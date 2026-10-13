import pytest
from src.shared.domain.entities.boletim_ga import Boletim_GA
from src.shared.helpers.errors.domain_errors import EntityError


class TestBoletimGA:

    def test_boletim_ga_basic_creation(self):
 
        boletim = Boletim_GA(
            current_tests=[6.0, 8.0],
            current_assignments=[7.0],
            num_remaining_tests=2,
            num_remaining_assignments=1,
            test_weight=0.6,
            assignment_weight=0.4
        )
        
        assert boletim.current_tests == [6.0, 8.0]
        assert boletim.current_assignments == [7.0]
        assert boletim.num_remaining_tests == 2
        assert boletim.num_remaining_assignments == 1
        assert boletim.test_weight == 0.6
        assert boletim.assignment_weight == 0.4
        assert boletim.spec_test_weight is None
        assert boletim.spec_assignment_weight is None

    def test_boletim_ga_with_specific_weights(self):

        boletim = Boletim_GA(
            current_tests=[6.0],
            current_assignments=[7.0],
            num_remaining_tests=2,
            num_remaining_assignments=2,
            test_weight=0.6,
            assignment_weight=0.4,
            spec_test_weight=[0.2, 0.4, 0.4],
            spec_assignment_weight=[0.3, 0.3, 0.4]
        )
        
        assert boletim.spec_test_weight == [0.2, 0.4, 0.4]
        assert boletim.spec_assignment_weight == [0.3, 0.3, 0.4]

    def test_boletim_ga_only_tests(self):

        boletim = Boletim_GA(
            current_tests=[5.0],
            current_assignments=[],
            num_remaining_tests=3,
            num_remaining_assignments=0,
            test_weight=1.0,
            assignment_weight=0.0
        )
        
        assert len(boletim.current_tests) == 1
        assert len(boletim.current_assignments) == 0
        assert boletim.test_weight == 1.0
        assert boletim.assignment_weight == 0.0

    def test_boletim_ga_only_assignments(self):

        boletim = Boletim_GA(
            current_tests=[],
            current_assignments=[8.0, 9.0],
            num_remaining_tests=0,
            num_remaining_assignments=2,
            test_weight=0.0,
            assignment_weight=1.0
        )
        
        assert len(boletim.current_tests) == 0
        assert len(boletim.current_assignments) == 2
        assert boletim.test_weight == 0.0
        assert boletim.assignment_weight == 1.0

    def test_boletim_ga_custom_max_grade(self):

        boletim = Boletim_GA(
            current_tests=[50.0, 60.0],
            current_assignments=[70.0],
            num_remaining_tests=2,
            num_remaining_assignments=1,
            test_weight=0.6,
            assignment_weight=0.4,
            max_grade=100.0
        )
        
        assert boletim.current_tests == [50.0, 60.0]
        assert boletim.current_assignments == [70.0]

    def test_boletim_ga_to_dict(self):

        boletim = Boletim_GA(
            current_tests=[6.0],
            current_assignments=[7.0],
            num_remaining_tests=2,
            num_remaining_assignments=1,
            test_weight=0.6,
            assignment_weight=0.4
        )
        
        result = boletim.to_dict()
        
        assert isinstance(result, dict)
        assert result["current_tests"] == [6.0]
        assert result["current_assignments"] == [7.0]
        assert result["num_remaining_tests"] == 2
        assert result["num_remaining_assignments"] == 1
        assert result["test_weight"] == 0.6
        assert result["assignment_weight"] == 0.4
        assert result["spec_test_weight"] is None
        assert result["spec_assignment_weight"] is None

    def test_boletim_ga_validate_num_remaining_valid(self):

        assert Boletim_GA.validate_num_remaining(0) == True
        assert Boletim_GA.validate_num_remaining(5) == True
        assert Boletim_GA.validate_num_remaining(100) == True

    def test_boletim_ga_validate_num_remaining_invalid(self):

        assert Boletim_GA.validate_num_remaining(-1) == False
        assert Boletim_GA.validate_num_remaining(-10) == False
        assert Boletim_GA.validate_num_remaining(1.5) == False
        assert Boletim_GA.validate_num_remaining("5") == False

    def test_boletim_ga_validate_weights_valid(self):

        assert Boletim_GA.validate_weights(0.0) == True
        assert Boletim_GA.validate_weights(0.5) == True
        assert Boletim_GA.validate_weights(1.0) == True
        assert Boletim_GA.validate_weights(0.6) == True

    def test_boletim_ga_validate_weights_invalid(self):

        assert Boletim_GA.validate_weights(-0.1) == False
        assert Boletim_GA.validate_weights(1.5) == False
        assert Boletim_GA.validate_weights("0.5") == False
        assert Boletim_GA.validate_weights(None) == False

    def test_boletim_ga_validate_tests_valid(self):

        assert Boletim_GA.validate_tests([6.0, 8.0], 10.0) == True
        assert Boletim_GA.validate_tests([0.0, 5.0, 10.0], 10.0) == True
        assert Boletim_GA.validate_tests([6.5, 7.5], 10.0) == True
        assert Boletim_GA.validate_tests([], 10.0) == True

    def test_boletim_ga_validate_tests_invalid(self):

        assert Boletim_GA.validate_tests([6.3], 10.0) == False  # Não é múltiplo de 0.5
        assert Boletim_GA.validate_tests([-1.0], 10.0) == False  # Negativo
        assert Boletim_GA.validate_tests([11.0], 10.0) == False  # Acima do máximo
        assert Boletim_GA.validate_tests("not a list", 10.0) == False
        assert Boletim_GA.validate_tests([6.0, "8.0"], 10.0) == False

    def test_boletim_ga_validate_spec_weights_valid(self):
 
        assert Boletim_GA.validate_spec_weights([0.2, 0.4, 0.4]) == True
        assert Boletim_GA.validate_spec_weights([0.5, 0.5]) == True
        assert Boletim_GA.validate_spec_weights([1.0]) == True
        assert Boletim_GA.validate_spec_weights([0.0, 0.0, 1.0]) == True

    def test_boletim_ga_validate_spec_weights_invalid(self):
  
        assert Boletim_GA.validate_spec_weights([0.2, -0.4, 0.4]) == False  # Negativo
        assert Boletim_GA.validate_spec_weights([0.5, 1.5]) == False  # Acima de 1
        assert Boletim_GA.validate_spec_weights("not a list") == False
        assert Boletim_GA.validate_spec_weights([0.5, "0.5"]) == False

    def test_boletim_ga_validate_sum_weights_valid(self):

        assert Boletim_GA.validate_sum_weights(0.6, 0.4) == True
        assert Boletim_GA.validate_sum_weights(0.5, 0.5) == True
        assert Boletim_GA.validate_sum_weights(1.0, 0.0) == True
        assert Boletim_GA.validate_sum_weights(0.7, 0.3) == True

    def test_boletim_ga_validate_sum_weights_invalid(self):

        assert Boletim_GA.validate_sum_weights(0.5, 0.6) == False
        assert Boletim_GA.validate_sum_weights(0.3, 0.3) == False
        assert Boletim_GA.validate_sum_weights(1.0, 1.0) == False

    def test_boletim_ga_validate_sum_spec_weights_valid(self):
   
        assert Boletim_GA.validate_sum_spec_weights([0.5, 0.5], [6.0], 1) == True
        assert Boletim_GA.validate_sum_spec_weights([0.2, 0.3, 0.5], [6.0, 7.0], 1) == True
        assert Boletim_GA.validate_sum_spec_weights(None, [6.0], 1) == True

    def test_boletim_ga_validate_sum_spec_weights_invalid_length(self):

        assert Boletim_GA.validate_sum_spec_weights([0.5, 0.5], [6.0], 2) == False
        assert Boletim_GA.validate_sum_spec_weights([0.5], [6.0], 1) == False

    def test_boletim_ga_validate_sum_spec_weights_invalid_sum(self):

        assert Boletim_GA.validate_sum_spec_weights([0.3, 0.3], [6.0], 1) == False
        assert Boletim_GA.validate_sum_spec_weights([0.5, 0.6], [6.0], 1) == False

    def test_boletim_ga_invalid_num_remaining_tests(self):
  
        with pytest.raises(EntityError):
            Boletim_GA(
                current_tests=[6.0],
                current_assignments=[7.0],
                num_remaining_tests=-1,
                num_remaining_assignments=1,
                test_weight=0.6,
                assignment_weight=0.4
            )

    def test_boletim_ga_invalid_num_remaining_assignments(self):

        with pytest.raises(EntityError):
            Boletim_GA(
                current_tests=[6.0],
                current_assignments=[7.0],
                num_remaining_tests=1,
                num_remaining_assignments=-1,
                test_weight=0.6,
                assignment_weight=0.4
            )

    def test_boletim_ga_invalid_test_weight(self):

        with pytest.raises(EntityError):
            Boletim_GA(
                current_tests=[6.0],
                current_assignments=[7.0],
                num_remaining_tests=1,
                num_remaining_assignments=1,
                test_weight=1.5,
                assignment_weight=0.4
            )

    def test_boletim_ga_invalid_assignment_weight(self):

        with pytest.raises(EntityError):
            Boletim_GA(
                current_tests=[6.0],
                current_assignments=[7.0],
                num_remaining_tests=1,
                num_remaining_assignments=1,
                test_weight=0.6,
                assignment_weight=-0.1
            )

    def test_boletim_ga_invalid_weights_sum(self):

        with pytest.raises(EntityError):
            Boletim_GA(
                current_tests=[6.0],
                current_assignments=[7.0],
                num_remaining_tests=1,
                num_remaining_assignments=1,
                test_weight=0.5,
                assignment_weight=0.6
            )

    def test_boletim_ga_invalid_current_tests(self):

        with pytest.raises(EntityError):
            Boletim_GA(
                current_tests=[6.3],  # Não é múltiplo de 0.5
                current_assignments=[7.0],
                num_remaining_tests=1,
                num_remaining_assignments=1,
                test_weight=0.6,
                assignment_weight=0.4
            )

    def test_boletim_ga_invalid_current_assignments(self):

        with pytest.raises(EntityError):
            Boletim_GA(
                current_tests=[6.0],
                current_assignments=[15.0],  # Acima do máximo
                num_remaining_tests=1,
                num_remaining_assignments=1,
                test_weight=0.6,
                assignment_weight=0.4
            )

    def test_boletim_ga_invalid_spec_test_weight_length(self):

        with pytest.raises(EntityError):
            Boletim_GA(
                current_tests=[6.0],
                current_assignments=[7.0],
                num_remaining_tests=2,
                num_remaining_assignments=1,
                test_weight=0.6,
                assignment_weight=0.4,
                spec_test_weight=[0.5, 0.5]  # Deveria ter 3 elementos
            )

    def test_boletim_ga_invalid_spec_test_weight_sum(self):

        with pytest.raises(EntityError):
            Boletim_GA(
                current_tests=[6.0],
                current_assignments=[7.0],
                num_remaining_tests=2,
                num_remaining_assignments=1,
                test_weight=0.6,
                assignment_weight=0.4,
                spec_test_weight=[0.3, 0.3, 0.3]  # Soma = 0.9, deveria ser 1.0
            )

    def test_boletim_ga_invalid_spec_test_weight_values(self):
  
        with pytest.raises(EntityError):
            Boletim_GA(
                current_tests=[6.0],
                current_assignments=[7.0],
                num_remaining_tests=2,
                num_remaining_assignments=1,
                test_weight=0.6,
                assignment_weight=0.4,
                spec_test_weight=[0.5, -0.5, 1.0]  # Valor negativo
            )

    def test_boletim_ga_invalid_spec_assignment_weight_length(self):
    
        with pytest.raises(EntityError):
            Boletim_GA(
                current_tests=[6.0],
                current_assignments=[7.0],
                num_remaining_tests=1,
                num_remaining_assignments=2,
                test_weight=0.6,
                assignment_weight=0.4,
                spec_assignment_weight=[0.5, 0.5]  # Deveria ter 3 elementos
            )

    def test_boletim_ga_invalid_spec_assignment_weight_sum(self):
     
        with pytest.raises(EntityError):
            Boletim_GA(
                current_tests=[6.0],
                current_assignments=[7.0],
                num_remaining_tests=1,
                num_remaining_assignments=2,
                test_weight=0.6,
                assignment_weight=0.4,
                spec_assignment_weight=[0.4, 0.4, 0.4]  # Soma = 1.2
            )

    def test_boletim_ga_valid_grades_multiples_of_half(self):
    
        boletim = Boletim_GA(
            current_tests=[0.0, 0.5, 1.0, 5.5, 10.0],
            current_assignments=[6.5, 7.0, 8.5],
            num_remaining_tests=0,
            num_remaining_assignments=0,
            test_weight=0.6,
            assignment_weight=0.4
        )
        
        assert boletim.current_tests == [0.0, 0.5, 1.0, 5.5, 10.0]
        assert boletim.current_assignments == [6.5, 7.0, 8.5]

    def test_boletim_ga_empty_lists(self):
    
        boletim = Boletim_GA(
            current_tests=[],
            current_assignments=[],
            num_remaining_tests=3,
            num_remaining_assignments=2,
            test_weight=0.5,
            assignment_weight=0.5
        )
        
        assert boletim.current_tests == []
        assert boletim.current_assignments == []
        assert boletim.num_remaining_tests == 3
        assert boletim.num_remaining_assignments == 2

    def test_boletim_ga_response_attribute(self):
        
        boletim = Boletim_GA(
            current_tests=[6.0],
            current_assignments=[7.0],
            num_remaining_tests=1,
            num_remaining_assignments=1,
            test_weight=0.6,
            assignment_weight=0.4
        )
        
        assert hasattr(boletim, 'response')
        assert isinstance(boletim.response, dict)
        assert boletim.response == boletim.to_dict()