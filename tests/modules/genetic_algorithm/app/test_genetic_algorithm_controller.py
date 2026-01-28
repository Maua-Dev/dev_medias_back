import pytest
from src.modules.genetic_algorithm.app.genetic_algorithm_controller import GeneticAlgorithmController
from src.modules.genetic_algorithm.app.genetic_algorithm_usecase import GeneticAlgorithmUsecase
from src.shared.helpers.external_interfaces.http_models import HttpRequest


class TestGeneticAlgorithmController:

    def test_genetic_algorithm_controller_basic(self):
        request = HttpRequest(body={
            'current_tests': [6.0, 8.0],
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 200
        assert 'tests' in response.body
        assert 'assignments' in response.body

    def test_genetic_algorithm_controller_only_tests(self):
        request = HttpRequest(body={
            'current_tests': [5.0],
            'current_assignments': [],
            'num_remaining_tests': 3,
            'num_remaining_assignments': 0,
            'test_weight': 1.0,
            'assignment_weight': 0.0,
            'target_average': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 200

    def test_genetic_algorithm_controller_only_assignments(self):
        request = HttpRequest(body={
            'current_tests': [],
            'current_assignments': [8.0, 9.0],
            'num_remaining_tests': 0,
            'num_remaining_assignments': 2,
            'test_weight': 0.0,
            'assignment_weight': 1.0,
            'target_average': 6.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 200

    def test_genetic_algorithm_controller_with_custom_parameters(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': 7.0,
            'max_grade': 10.0,
            'population_size': 200,
            'generations': 300
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 200

    def test_genetic_algorithm_controller_with_specific_weights(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 2,
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': 7.0,
            'spec_test_weight': [0.2, 0.4, 0.4],
            'spec_assingment_weight': [0.3, 0.3, 0.4]
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 200

    def test_genetic_algorithm_controller_current_tests_missing(self):
        request = HttpRequest(body={
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro current_tests não existe'

    def test_genetic_algorithm_controller_current_tests_wrong_type(self):
        request = HttpRequest(body={
            'current_tests': 6.0,
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert 'Parâmetro current_tests não possui tipo correto' in response.body

    def test_genetic_algorithm_controller_current_tests_item_wrong_type(self):
        request = HttpRequest(body={
            'current_tests': [6.0, '8.0'],
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400

    def test_genetic_algorithm_controller_current_tests_item_none(self):
        request = HttpRequest(body={
            'current_tests': [6.0, None],
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400

    def test_genetic_algorithm_controller_current_assignments_missing(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro current_assignments não existe'

    def test_genetic_algorithm_controller_current_assignments_wrong_type(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': 7.0,
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert 'Parâmetro current_assignments não possui tipo correto' in response.body

    def test_genetic_algorithm_controller_current_assignments_item_wrong_type(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0, '8.0'],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400

    def test_genetic_algorithm_controller_num_remaining_tests_missing(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0],
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro num_remaining_tests não existe'

    def test_genetic_algorithm_controller_num_remaining_tests_wrong_type(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0],
            'num_remaining_tests': '2',
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert 'Parâmetro num_remaining_tests não possui tipo correto' in response.body

    def test_genetic_algorithm_controller_num_remaining_tests_negative(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0],
            'num_remaining_tests': -1,
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert 'Must be non-negative' in response.body

    def test_genetic_algorithm_controller_num_remaining_assignments_missing(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro num_remaining_assignments não existe'

    def test_genetic_algorithm_controller_num_remaining_assignments_wrong_type(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': '1',
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert 'Parâmetro num_remaining_assignments não possui tipo correto' in response.body

    def test_genetic_algorithm_controller_num_remaining_assignments_negative(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': -1,
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert 'Must be non-negative' in response.body

    def test_genetic_algorithm_controller_test_weight_missing(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'assignment_weight': 0.4,
            'target_average': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro test_weight não existe'

    def test_genetic_algorithm_controller_test_weight_wrong_type(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'test_weight': '0.6',
            'assignment_weight': 0.4,
            'target_average': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert 'Parâmetro test_weight não possui tipo correto' in response.body

    def test_genetic_algorithm_controller_test_weight_out_of_range(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'test_weight': 1.5,
            'assignment_weight': 0.4,
            'target_average': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert 'Must be between 0 and 1' in response.body

    def test_genetic_algorithm_controller_assignment_weight_missing(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'target_average': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro assignment_weight não existe'

    def test_genetic_algorithm_controller_assignment_weight_wrong_type(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'assignment_weight': '0.4',
            'target_average': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert 'Parâmetro assignment_weight não possui tipo correto' in response.body

    def test_genetic_algorithm_controller_assignment_weight_out_of_range(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'assignment_weight': -0.1,
            'target_average': 7.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert 'Must be between 0 and 1' in response.body

    def test_genetic_algorithm_controller_target_average_missing(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'assignment_weight': 0.4
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert response.body == 'Parâmetro target_average não existe'

    def test_genetic_algorithm_controller_target_average_wrong_type(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': '7.0'
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert 'Parâmetro target_average não possui tipo correto' in response.body

    def test_genetic_algorithm_controller_target_average_out_of_range(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': 15.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert 'Must be between 0 and 10' in response.body

    def test_genetic_algorithm_controller_max_grade_wrong_type(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': 7.0,
            'max_grade': '10.0'
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert 'Parâmetro max_grade não possui tipo correto' in response.body

    def test_genetic_algorithm_controller_max_grade_invalid(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': 7.0,
            'max_grade': -5.0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert 'Must be greater than 0' in response.body

    def test_genetic_algorithm_controller_population_size_wrong_type(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': 7.0,
            'population_size': '100'
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert 'Parâmetro population_size não possui tipo correto' in response.body

    def test_genetic_algorithm_controller_population_size_invalid(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': 7.0,
            'population_size': -10
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert 'Must be greater than 0' in response.body

    def test_genetic_algorithm_controller_generations_wrong_type(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': 7.0,
            'generations': '200'
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert 'Parâmetro generations não possui tipo correto' in response.body

    def test_genetic_algorithm_controller_generations_invalid(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': 7.0,
            'generations': 0
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert 'Must be greater than 0' in response.body

    def test_genetic_algorithm_controller_spec_test_weight_wrong_type(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': 7.0,
            'spec_test_weight': 'wrong'
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert 'Parâmetro spec_test_weight não possui tipo correto' in response.body

    def test_genetic_algorithm_controller_spec_test_weight_wrong_length(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': 7.0,
            'spec_test_weight': [0.5, 0.5]
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert 'Must have the same length' in response.body

    def test_genetic_algorithm_controller_spec_test_weight_item_wrong_type(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': 7.0,
            'spec_test_weight': [0.3, '0.3', 0.4]
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400

    def test_genetic_algorithm_controller_spec_test_weight_sum_not_one(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': 7.0,
            'spec_test_weight': [0.3, 0.3, 0.3]
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert 'The sum must be equal to 1' in response.body

    def test_genetic_algorithm_controller_spec_assingment_weight_wrong_type(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': 7.0,
            'spec_assingment_weight': 'wrong'
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert 'Parâmetro spec_assingment_weight não possui tipo correto' in response.body

    def test_genetic_algorithm_controller_spec_assingment_weight_wrong_length(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': 7.0,
            'spec_assingment_weight': [0.5, 0.5]
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert 'Must have the same length' in response.body

    def test_genetic_algorithm_controller_spec_assingment_weight_item_wrong_type(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': 7.0,
            'spec_assingment_weight': [0.3, '0.3', 0.4]
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400

    def test_genetic_algorithm_controller_spec_assingment_weight_sum_not_one(self):
        request = HttpRequest(body={
            'current_tests': [6.0],
            'current_assignments': [7.0],
            'num_remaining_tests': 2,
            'num_remaining_assignments': 1,
            'test_weight': 0.6,
            'assignment_weight': 0.4,
            'target_average': 7.0,
            'spec_assingment_weight': [0.3, 0.3, 0.3]
        })

        usecase = GeneticAlgorithmUsecase()
        controller = GeneticAlgorithmController(usecase=usecase)

        response = controller(request=request)

        assert response.status_code == 400
        assert 'The sum must be equal to 1' in response.body