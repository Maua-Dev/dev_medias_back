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

    def test_returns_boletim(self):
        boletim = self._run()
        assert boletim is not None

    def test_boletim_has_provas(self):
        boletim = self._run()
        assert hasattr(boletim, 'provas')
        assert isinstance(boletim.provas, list)

    def test_boletim_has_trabalhos(self):
        boletim = self._run()
        assert hasattr(boletim, 'trabalhos')
        assert isinstance(boletim.trabalhos, list)

    def test_boletim_has_message(self):
        boletim = self._run()
        assert hasattr(boletim, 'message')
        assert isinstance(boletim.message, str)

    def test_provas_total_length(self):
        boletim = self._run(num_remaining_tests=2)
        # current(2) + remaining(2)
        assert len(boletim.provas) == 4

    def test_trabalhos_total_length(self):
        boletim = self._run(num_remaining_assignments=2)
        # current(2) + remaining(2)
        assert len(boletim.trabalhos) == 4

    def test_provas_have_valor_and_peso(self):
        boletim = self._run()
        for prova in boletim.provas:
            assert 'valor' in prova
            assert 'peso' in prova

    def test_trabalhos_have_valor_and_peso(self):
        boletim = self._run()
        for trabalho in boletim.trabalhos:
            assert 'valor' in trabalho
            assert 'peso' in trabalho

    def test_final_avg_within_range(self):
        boletim = self._run()
        assert 0.0 <= boletim.final_avg <= 10.0

    def test_target_avg_stored(self):
        boletim = self._run(target_average=8.0)
        assert boletim.target_avg == 8.0

    def test_grades_rounded_to_2_decimals(self):
        boletim = self._run()
        for prova in boletim.provas:
            assert prova['valor'] == round(prova['valor'], 2)
            assert prova['peso'] == round(prova['peso'], 2)

    def test_message_exact_when_diff_lte_005(self):
        boletim = self._run(target_average=7.0, current_tests=[7.0, 7.0], current_assignments=[7.0, 7.0])
        if abs(boletim.final_avg - boletim.target_avg) <= 0.05:
            assert boletim.message == "O algoritmo retornou uma combinação válida de notas"

    def test_message_contains_diff_when_close(self):
        boletim = self._run()
        diff = abs(boletim.final_avg - boletim.target_avg)
        if 0.05 < diff <= 0.2:
            assert "próxima" in boletim.message

    def test_message_contains_diff_when_far(self):
        boletim = self._run()
        diff = abs(boletim.final_avg - boletim.target_avg)
        if diff > 0.2:
            assert "não conseguiu" in boletim.message

    # ==========================================
    # Casos de erro
    # ==========================================

    def test_raises_combination_not_found_when_impossible(self):
        with patch('src.modules.genetic_algorithm.app.genetic_algorithm_usecase.GradeGeneticAlgorithm') as mock_ga:
            mock_instance = MagicMock()
            mock_instance.run.return_value = (None, None, None)
            mock_ga.return_value = mock_instance
            with pytest.raises(CombinationNotFound):
                self._run()

    def test_raises_entity_error_invalid_weight_sum(self):
        from src.shared.helpers.errors.domain_errors import EntityError
        with pytest.raises(EntityError):
            self._run(test_weight=0.5, assignment_weight=0.3)

    def test_raises_entity_error_negative_num_remaining_tests(self):
        from src.shared.helpers.errors.domain_errors import EntityError
        with pytest.raises(EntityError):
            self._run(num_remaining_tests=-1)

    def test_raises_entity_error_negative_num_remaining_assignments(self):
        from src.shared.helpers.errors.domain_errors import EntityError
        with pytest.raises(EntityError):
            self._run(num_remaining_assignments=-1)

    def test_raises_entity_error_invalid_spec_weight_sum(self):
        from src.shared.helpers.errors.domain_errors import EntityError
        with pytest.raises(EntityError):
            self._run(spec_test_weight=[0.5, 0.5, 0.5, 0.5])

    def test_raises_entity_error_spec_weight_wrong_length(self):
        from src.shared.helpers.errors.domain_errors import EntityError
        with pytest.raises(EntityError):
            self._run(spec_test_weight=[0.5, 0.5])

    def test_raises_entity_error_grade_above_max(self):
        from src.shared.helpers.errors.domain_errors import EntityError
        with pytest.raises(EntityError):
            self._run(current_tests=[11.0, 8.0])

    def test_raises_entity_error_grade_below_zero(self):
        from src.shared.helpers.errors.domain_errors import EntityError
        with pytest.raises(EntityError):
            self._run(current_tests=[-1.0, 8.0])