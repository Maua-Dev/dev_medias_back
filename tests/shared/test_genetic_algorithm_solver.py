from src.shared.domain.entities.boletim_ga import Boletim_GA
from src.shared.genetic_algorithm_solver import GradeGeneticAlgorithm


def _ga_one_test_one_assignment(target_average: float = 2.5) -> GradeGeneticAlgorithm:
    """Setup com 1 lacuna de prova + 1 de trabalho e pesos iguais."""
    boletim = Boletim_GA(
        current_tests=[],
        current_assignments=[],
        num_remaining_tests=1,
        num_remaining_assignments=1,
        test_weight=0.5,
        assignment_weight=0.5,
        spec_test_weight=[1.0],
        spec_assignment_weight=[1.0],
    )
    return GradeGeneticAlgorithm(boletim=boletim, target_average=target_average)


def _ind(test: float, assignment: float) -> dict:
    return {"tests": [test], "assignments": [assignment]}


class TestGradeGeneticAlgorithmFitnessBalance:

    def test_balanced_better_than_mild_imbalance(self):
        ga = _ga_one_test_one_assignment(target_average=2.5)
        assert ga.fitness(_ind(2.5, 2.5)) < ga.fitness(_ind(1.5, 3.5))

    def test_mild_imbalance_better_than_extreme_assignment_heavy(self):
        ga = _ga_one_test_one_assignment(target_average=2.5)
        assert ga.fitness(_ind(1.5, 3.5)) < ga.fitness(_ind(0.5, 4.5))

    def test_balanced_better_than_extreme_test_heavy(self):
        ga = _ga_one_test_one_assignment(target_average=2.5)
        assert ga.fitness(_ind(2.5, 2.5)) < ga.fitness(_ind(4.5, 0.5))

    def test_balanced_better_than_extreme_assignment_heavy(self):
        ga = _ga_one_test_one_assignment(target_average=2.5)
        assert ga.fitness(_ind(2.5, 2.5)) < ga.fitness(_ind(0.5, 4.5))


class TestGradeGeneticAlgorithmFitnessAssignmentPreference:

    def test_mild_assignment_bias_beats_mirror(self):
        """1.5 prova / 3.5 trabalho deve ganhar do espelho 3.5 / 1.5."""
        ga = _ga_one_test_one_assignment(target_average=2.5)
        assert ga.fitness(_ind(1.5, 3.5)) < ga.fitness(_ind(3.5, 1.5))

    def test_extreme_assignment_bias_still_loses_to_balanced(self):
        ga = _ga_one_test_one_assignment(target_average=2.5)
        assert ga.fitness(_ind(2.5, 2.5)) < ga.fitness(_ind(0.5, 4.5))


class TestGradeGeneticAlgorithmFitnessTargetDominance:

    def test_far_from_target_worse_than_near_unbalanced(self):
        ga = _ga_one_test_one_assignment(target_average=2.5)
        far_balanced = _ind(0.0, 0.0)
        near_unbalanced = _ind(4.5, 0.5)
        assert ga.fitness(near_unbalanced) < ga.fitness(far_balanced)

    def test_undershoot_worse_than_equivalent_overshoot(self):
        ga = _ga_one_test_one_assignment(target_average=2.5)
        # avg 1.5 → undershoot 1.0; avg 3.5 → overshoot 1.0
        undershoot = _ind(1.5, 1.5)
        overshoot = _ind(3.5, 3.5)
        assert ga.fitness(overshoot) < ga.fitness(undershoot)


class TestGradeGeneticAlgorithmFitnessEdgeCases:

    def test_only_tests_remaining_does_not_crash(self):
        boletim = Boletim_GA(
            current_tests=[],
            current_assignments=[],
            num_remaining_tests=2,
            num_remaining_assignments=0,
            test_weight=1.0,
            assignment_weight=0.0,
            spec_test_weight=[0.5, 0.5],
            spec_assignment_weight=[],
        )
        ga = GradeGeneticAlgorithm(boletim=boletim, target_average=6.0)
        score = ga.fitness({"tests": [6.0, 6.0], "assignments": []})
        assert isinstance(score, float)
        assert score >= 0.0

    def test_only_assignments_remaining_does_not_crash(self):
        boletim = Boletim_GA(
            current_tests=[],
            current_assignments=[],
            num_remaining_tests=0,
            num_remaining_assignments=2,
            test_weight=0.0,
            assignment_weight=1.0,
            spec_test_weight=[],
            spec_assignment_weight=[0.5, 0.5],
        )
        ga = GradeGeneticAlgorithm(boletim=boletim, target_average=6.0)
        score = ga.fitness({"tests": [], "assignments": [6.0, 6.0]})
        assert isinstance(score, float)
        assert score >= 0.0

    def test_single_gap_does_not_crash(self):
        boletim = Boletim_GA(
            current_tests=[5.0],
            current_assignments=[],
            num_remaining_tests=1,
            num_remaining_assignments=0,
            test_weight=1.0,
            assignment_weight=0.0,
            spec_test_weight=[0.5, 0.5],
            spec_assignment_weight=[],
        )
        ga = GradeGeneticAlgorithm(boletim=boletim, target_average=6.0)
        score = ga.fitness({"tests": [7.0], "assignments": []})
        assert isinstance(score, float)
        assert score >= 0.0
