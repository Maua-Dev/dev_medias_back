import pytest
from unittest.mock import MagicMock, patch
from src.modules.genetic_algorithm.app.genetic_algorithm_usecase import GeneticAlgorithmUsecase
from src.shared.helpers.errors.usecase_errors import CombinationNotFound


class TestGeneticAlgorithmUsecase:

    def setup_method(self):
        self.usecase = GeneticAlgorithmUsecase()

    def _run(self, **kwargs):
        defaults = dict(
            current_tests=[7.0, 8.0],
            current_assignments=[6.0, 9.0],
            num_remaining_tests=2,
            num_remaining_assignments=2,
            test_weight=0.6,
            assignment_weight=0.4,
            target_average=7.0,
            spec_test_weight=[0.25, 0.25, 0.25, 0.25],
            spec_assignment_weight=[0.25, 0.25, 0.25, 0.25],
            max_grade=10.0,
            population_size=50,
            generations=50,
        )
        defaults.update(kwargs)
        return self.usecase(**defaults)

    # ==========================================
    # Casos de sucesso
    # ==========================================

    def test_returns_boletim_with_solution(self):
        boletim = self._run()
        assert boletim is not None
        assert hasattr(boletim, 'calculated_tests')
        assert hasattr(boletim, 'calculated_assignments')
        assert hasattr(boletim, 'final_avg')

    def test_calculated_tests_length(self):
        boletim = self._run(num_remaining_tests=2)
        assert len(boletim.calculated_tests) == 2

    def test_calculated_assignments_length(self):
        boletim = self._run(num_remaining_assignments=2)
        assert len(boletim.calculated_assignments) == 2

    def test_final_avg_within_range(self):
        boletim = self._run(target_average=7.0)
        assert 0.0 <= boletim.final_avg <= 10.0

    def test_target_avg_stored(self):
        boletim = self._run(target_average=8.0)
        assert boletim.target_avg == 8.0

    def test_only_tests_no_assignments(self):
        boletim = self._run(
            current_tests=[7.0, 8.0],
            current_assignments=[],
            num_remaining_tests=2,
            num_remaining_assignments=0,
            test_weight=1.0,
            assignment_weight=0.0,
            spec_test_weight=[0.25, 0.25, 0.25, 0.25],
            spec_assignment_weight=None,
        )
        assert boletim is not None
        assert len(boletim.calculated_assignments) == 0

    def test_only_assignments_no_tests(self):
        boletim = self._run(
            current_tests=[],
            current_assignments=[8.0, 9.0],
            num_remaining_tests=0,
            num_remaining_assignments=2,
            test_weight=0.0,
            assignment_weight=1.0,
            spec_test_weight=None,
            spec_assignment_weight=[0.25, 0.25, 0.25, 0.25],
        )
        assert boletim is not None
        assert len(boletim.calculated_tests) == 0

    def test_no_remaining_tests_or_assignments(self):
        boletim = self._run(
            current_tests=[7.0, 8.0],
            current_assignments=[6.0, 9.0],
            num_remaining_tests=0,
            num_remaining_assignments=0,
            spec_test_weight=[0.5, 0.5],
            spec_assignment_weight=[0.5, 0.5],
        )
        assert boletim is not None

    def test_high_target_average(self):
        boletim = self._run(target_average=9.5)
        assert boletim.target_avg == 9.5

    def test_low_target_average(self):
        boletim = self._run(target_average=1.0)
        assert boletim.final_avg >= 0.0

    def test_spec_weights_none(self):
        boletim = self._run(
            spec_test_weight=None,
            spec_assignment_weight=None,
        )
        assert boletim is not None

    # ==========================================
    # Casos de erro
    # ==========================================

    def test_raises_entity_error_invalid_test_weight_sum(self):
        from src.shared.helpers.errors.domain_errors import EntityError
        with pytest.raises(EntityError):
            self._run(test_weight=0.5, assignment_weight=0.3)

    def test_raises_entity_error_negative_num_remaining(self):
        from src.shared.helpers.errors.domain_errors import EntityError
        with pytest.raises(EntityError):
            self._run(num_remaining_tests=-1)

    def test_raises_entity_error_invalid_spec_weight_sum(self):
        from src.shared.helpers.errors.domain_errors import EntityError
        with pytest.raises(EntityError):
            self._run(spec_test_weight=[0.5, 0.5, 0.5, 0.5])  # soma 2.0

    def test_raises_entity_error_spec_weight_wrong_length(self):
        from src.shared.helpers.errors.domain_errors import EntityError
        with pytest.raises(EntityError):
            self._run(spec_test_weight=[0.5, 0.5])  # length errado

    def test_raises_entity_error_grade_above_max(self):
        from src.shared.helpers.errors.domain_errors import EntityError
        with pytest.raises(EntityError):
            self._run(current_tests=[11.0, 8.0])

    def test_raises_entity_error_grade_below_zero(self):
        from src.shared.helpers.errors.domain_errors import EntityError
        with pytest.raises(EntityError):
            self._run(current_tests=[-1.0, 8.0])