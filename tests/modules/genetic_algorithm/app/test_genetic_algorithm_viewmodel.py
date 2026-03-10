# tests/modules/genetic_algorithm/app/test_genetic_algorithm_viewmodel.py

import pytest
from unittest.mock import MagicMock
from src.modules.genetic_algorithm.app.genetic_algorithm_viewmodel import GeneticAlgorithmViewmodel


def make_boletim(**kwargs):
    boletim = MagicMock()
    boletim.current_tests = kwargs.get('current_tests', [7.0, 8.0])
    boletim.current_assignments = kwargs.get('current_assignments', [6.0, 9.0])
    boletim.calculated_tests = kwargs.get('calculated_tests', [8.0, 7.5])
    boletim.calculated_assignments = kwargs.get('calculated_assignments', [7.0, 8.0])
    boletim.test_weight = kwargs.get('test_weight', 0.6)
    boletim.assignment_weight = kwargs.get('assignment_weight', 0.4)
    boletim.spec_test_weight = kwargs.get('spec_test_weight', [0.25, 0.25, 0.25, 0.25])
    boletim.spec_assignment_weight = kwargs.get('spec_assignment_weight', [0.25, 0.25, 0.25, 0.25])
    boletim.num_remaining_tests = kwargs.get('num_remaining_tests', 2)
    boletim.num_remaining_assignments = kwargs.get('num_remaining_assignments', 2)
    boletim.target_avg = kwargs.get('target_avg', 7.0)
    boletim.final_avg = kwargs.get('final_avg', 7.2)
    return boletim


class TestGeneticAlgorithmViewmodel:

    def test_to_dict_has_all_keys(self):
        vm = GeneticAlgorithmViewmodel(make_boletim())
        result = vm.to_dict()
        expected_keys = [
            "current_tests", "current_assignments",
            "tests", "assignments",
            "test_weight", "assignment_weight",
            "spec_test_weight", "spec_assignment_weight",
            "num_remaining_tests", "num_remaining_assignments",
            "target_average", "final_average",
            "calculated_tests", "calculated_assignments",
        ]
        for key in expected_keys:
            assert key in result, f"Missing key: {key}"

    def test_to_dict_values_match_boletim(self):
        boletim = make_boletim()
        result = GeneticAlgorithmViewmodel(boletim).to_dict()
        assert result["current_tests"] == boletim.current_tests
        assert result["current_assignments"] == boletim.current_assignments
        assert result["tests"] == boletim.calculated_tests
        assert result["assignments"] == boletim.calculated_assignments
        assert result["test_weight"] == boletim.test_weight
        assert result["assignment_weight"] == boletim.assignment_weight
        assert result["spec_test_weight"] == boletim.spec_test_weight
        assert result["spec_assignment_weight"] == boletim.spec_assignment_weight
        assert result["num_remaining_tests"] == boletim.num_remaining_tests
        assert result["num_remaining_assignments"] == boletim.num_remaining_assignments
        assert result["target_average"] == boletim.target_avg
        assert result["final_average"] == boletim.final_avg

    def test_tests_and_calculated_tests_are_same(self):
        result = GeneticAlgorithmViewmodel(make_boletim()).to_dict()
        assert result["tests"] == result["calculated_tests"]

    def test_assignments_and_calculated_assignments_are_same(self):
        result = GeneticAlgorithmViewmodel(make_boletim()).to_dict()
        assert result["assignments"] == result["calculated_assignments"]

    def test_spec_weights_none(self):
        boletim = make_boletim(spec_test_weight=None, spec_assignment_weight=None)
        result = GeneticAlgorithmViewmodel(boletim).to_dict()
        assert result["spec_test_weight"] is None
        assert result["spec_assignment_weight"] is None

    def test_empty_lists(self):
        boletim = make_boletim(
            current_tests=[], current_assignments=[],
            calculated_tests=[], calculated_assignments=[]
        )
        result = GeneticAlgorithmViewmodel(boletim).to_dict()
        assert result["current_tests"] == []
        assert result["tests"] == []

    def test_returns_dict_type(self):
        result = GeneticAlgorithmViewmodel(make_boletim()).to_dict()
        assert isinstance(result, dict)