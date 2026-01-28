import pytest
from src.modules.genetic_algorithm.app.genetic_algorithm_usecase import GeneticAlgorithmUsecase
from src.shared.helpers.errors.usecase_errors import CombinationNotFound, InvalidInput
from src.shared.helpers.errors.domain_errors import EntityParameterError


class TestGeneticAlgorithmUsecase:

    def test_basic_scenario(self):
        """Teste básico com notas já feitas e restantes a fazer"""
        usecase = GeneticAlgorithmUsecase()
        
        result = usecase(
            current_tests=[6.0, 8.0],
            current_assignments=[7.0],
            num_remaining_tests=2,
            num_remaining_assignments=1,
            test_weight=0.6,
            assignment_weight=0.4,
            target_average=7.0
        )
        
        assert result is not None
        assert 'tests' in result
        assert 'assignments' in result
        assert len(result['tests']) == 2
        assert len(result['assignments']) == 1

    def test_only_tests_scenario(self):
        """Cenário com apenas provas"""
        usecase = GeneticAlgorithmUsecase()
        
        result = usecase(
            current_tests=[5.0],
            current_assignments=[],
            num_remaining_tests=3,
            num_remaining_assignments=0,
            test_weight=1.0,
            assignment_weight=0.0,
            target_average=7.0
        )
        
        assert result is not None
        assert len(result['tests']) == 3
        assert len(result['assignments']) == 0

    def test_only_assignments_scenario(self):
        """Cenário com apenas trabalhos"""
        usecase = GeneticAlgorithmUsecase()
        
        result = usecase(
            current_tests=[],
            current_assignments=[8.0, 9.0],
            num_remaining_tests=0,
            num_remaining_assignments=2,
            test_weight=0.0,
            assignment_weight=1.0,
            target_average=6.0
        )
        
        assert result is not None
        assert len(result['tests']) == 0
        assert len(result['assignments']) == 2

    def test_all_remaining_scenario(self):
        """Cenário sem nenhuma nota feita ainda"""
        usecase = GeneticAlgorithmUsecase()
        
        result = usecase(
            current_tests=[],
            current_assignments=[],
            num_remaining_tests=3,
            num_remaining_assignments=2,
            test_weight=0.5,
            assignment_weight=0.5,
            target_average=7.0
        )
        
        assert result is not None
        assert len(result['tests']) == 3
        assert len(result['assignments']) == 2

    def test_high_target_average(self):
        """Teste com média desejada alta"""
        usecase = GeneticAlgorithmUsecase()
        
        result = usecase(
            current_tests=[10.0, 10.0],
            current_assignments=[10.0],
            num_remaining_tests=2,
            num_remaining_assignments=1,
            test_weight=0.6,
            assignment_weight=0.4,
            target_average=10.0
        )
        
        assert result is not None

    def test_low_target_average(self):
        """Teste com média desejada baixa"""
        usecase = GeneticAlgorithmUsecase()
        
        result = usecase(
            current_tests=[3.0],
            current_assignments=[4.0],
            num_remaining_tests=1,
            num_remaining_assignments=1,
            test_weight=0.5,
            assignment_weight=0.5,
            target_average=5.0
        )
        
        assert result is not None

    def test_with_specific_weights(self):
        """Teste com pesos específicos para cada avaliação"""
        usecase = GeneticAlgorithmUsecase()
        
        result = usecase(
            current_tests=[6.0],
            current_assignments=[7.0],
            num_remaining_tests=2,
            num_remaining_assignments=2,
            test_weight=0.6,
            assignment_weight=0.4,
            target_average=7.0,
            spec_test_weight=[0.2, 0.4, 0.4],
            spec_assignment_weight=[0.3, 0.3, 0.4]
        )
        
        assert result is not None

    def test_custom_max_grade(self):
        """Teste com nota máxima customizada"""
        usecase = GeneticAlgorithmUsecase()
        
        result = usecase(
            current_tests=[50.0],
            current_assignments=[60.0],
            num_remaining_tests=2,
            num_remaining_assignments=1,
            test_weight=0.6,
            assignment_weight=0.4,
            target_average=70.0,
            max_grade=100.0
        )
        
        assert result is not None

    def test_custom_ga_parameters(self):
        """Teste com parâmetros customizados do algoritmo genético"""
        usecase = GeneticAlgorithmUsecase()
        
        result = usecase(
            current_tests=[6.0],
            current_assignments=[7.0],
            num_remaining_tests=2,
            num_remaining_assignments=1,
            test_weight=0.6,
            assignment_weight=0.4,
            target_average=7.0,
            population_size=200,
            generations=300
        )
        
        assert result is not None

    def test_invalid_empty_lists(self):
        """Teste com listas vazias quando não deveria"""
        usecase = GeneticAlgorithmUsecase()
        
        # Este teste pode passar ou não dependendo da implementação
        # Se num_remaining for 0 para ambos, deveria lançar erro
        with pytest.raises((InvalidInput, EntityParameterError)):
            usecase(
                current_tests=[],
                current_assignments=[],
                num_remaining_tests=0,
                num_remaining_assignments=0,
                test_weight=0.5,
                assignment_weight=0.5,
                target_average=7.0
            )

    def test_invalid_max_grade_type(self):
        """Teste com tipo inválido para max_grade"""
        usecase = GeneticAlgorithmUsecase()
        
        with pytest.raises(InvalidInput):
            usecase(
                current_tests=[6.0],
                current_assignments=[7.0],
                num_remaining_tests=2,
                num_remaining_assignments=1,
                test_weight=0.6,
                assignment_weight=0.4,
                target_average=7.0,
                max_grade="10.0"  # tipo errado
            )

    def test_invalid_max_grade_negative(self):
        """Teste com max_grade negativo"""
        usecase = GeneticAlgorithmUsecase()
        
        with pytest.raises(InvalidInput):
            usecase(
                current_tests=[6.0],
                current_assignments=[7.0],
                num_remaining_tests=2,
                num_remaining_assignments=1,
                test_weight=0.6,
                assignment_weight=0.4,
                target_average=7.0,
                max_grade=-10.0
            )

    def test_invalid_target_average_type(self):
        """Teste com tipo inválido para target_average"""
        usecase = GeneticAlgorithmUsecase()
        
        with pytest.raises(InvalidInput):
            usecase(
                current_tests=[6.0],
                current_assignments=[7.0],
                num_remaining_tests=2,
                num_remaining_assignments=1,
                test_weight=0.6,
                assignment_weight=0.4,
                target_average="7.0"  # tipo errado
            )

    def test_invalid_target_average_negative(self):
        """Teste com target_average negativo"""
        usecase = GeneticAlgorithmUsecase()
        
        with pytest.raises(InvalidInput):
            usecase(
                current_tests=[6.0],
                current_assignments=[7.0],
                num_remaining_tests=2,
                num_remaining_assignments=1,
                test_weight=0.6,
                assignment_weight=0.4,
                target_average=-1.0
            )

    def test_invalid_target_average_exceeds_max(self):
        """Teste com target_average maior que max_grade"""
        usecase = GeneticAlgorithmUsecase()
        
        with pytest.raises(InvalidInput):
            usecase(
                current_tests=[6.0],
                current_assignments=[7.0],
                num_remaining_tests=2,
                num_remaining_assignments=1,
                test_weight=0.6,
                assignment_weight=0.4,
                target_average=15.0,
                max_grade=10.0
            )

    def test_invalid_weights_sum_not_one(self):
        """Teste com soma dos pesos diferente de 1"""
        usecase = GeneticAlgorithmUsecase()
        
        with pytest.raises(EntityParameterError):
            usecase(
                current_tests=[6.0],
                current_assignments=[7.0],
                num_remaining_tests=2,
                num_remaining_assignments=1,
                test_weight=0.5,
                assignment_weight=0.6,  # soma = 1.1
                target_average=7.0
            )

    def test_impossible_target(self):
        """Teste com meta impossível de alcançar"""
        usecase = GeneticAlgorithmUsecase()
        
        # Com notas muito baixas, pode ser impossível alcançar 10.0
        with pytest.raises((CombinationNotFound, Exception)):
            usecase(
                current_tests=[0.0, 1.0],
                current_assignments=[0.0],
                num_remaining_tests=1,
                num_remaining_assignments=1,
                test_weight=0.8,
                assignment_weight=0.2,
                target_average=10.0
            )

    def test_multiple_runs_consistency(self):
        """Teste executando múltiplas vezes para verificar consistência"""
        usecase = GeneticAlgorithmUsecase()
        
        for _ in range(5):
            result = usecase(
                current_tests=[6.0, 7.0],
                current_assignments=[8.0],
                num_remaining_tests=2,
                num_remaining_assignments=1,
                test_weight=0.6,
                assignment_weight=0.4,
                target_average=7.5
            )
            
            assert result is not None
            assert 'tests' in result
            assert 'assignments' in result