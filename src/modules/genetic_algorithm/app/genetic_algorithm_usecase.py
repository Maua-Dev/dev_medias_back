from src.shared.domain.entities.boletim_ga import Boletim_GA
from src.shared.helpers.errors.usecase_errors import CombinationNotFound
from src.shared.genetic_algorithm_solver import GradeGeneticAlgorithm
from decimal import Decimal, ROUND_HALF_DOWN


EXACT_DIFF_THRESHOLD = 0.05
CLOSE_DIFF_THRESHOLD = 0.2


def _round_grade_for_front(value: float) -> float:
    """
    Applies Maua display rule for grades:
    - output only in 0.5 steps (e.g. 5.5, 6.0)
    - midpoint ties do not round up
    """
    doubled = Decimal(str(value)) * Decimal("2")
    rounded_doubled = doubled.quantize(Decimal("1"), rounding=ROUND_HALF_DOWN)
    return float(rounded_doubled / Decimal("2"))


def _weight_for_front(value: float) -> float:
    """
    Preserva o peso enviado (até 4 casas) para não quebrar a soma (=1.0).
    Ex.: 0.25 permanece 0.25 (não vira 0.2).
    """
    return float(Decimal(str(value)).quantize(Decimal("0.0001")))


class GeneticAlgorithmUsecase:
    def __init__(self):
        pass

    def __call__(
        self,
        current_tests: list[float],
        current_assignments: list[float],
        num_remaining_tests: int,
        num_remaining_assignments: int,
        test_weight: float,
        assignment_weight: float,
        target_average: float,
        spec_test_weight: list[float],
        spec_assignment_weight: list[float],
        max_grade: float = 10.0,
        population_size: int = 150,
        generations: int = 200,
    ) -> Boletim_GA:

        boletim = Boletim_GA(
            current_tests=current_tests,
            current_assignments=current_assignments,
            num_remaining_tests=num_remaining_tests,
            num_remaining_assignments=num_remaining_assignments,
            test_weight=test_weight,
            assignment_weight=assignment_weight,
            spec_test_weight=spec_test_weight,
            spec_assignment_weight=spec_assignment_weight,
            max_grade=max_grade,
        )

        ga = GradeGeneticAlgorithm(
            boletim=boletim,
            target_average=target_average,
            max_grade=max_grade,
            population_size=population_size,
            generations=generations,
        )

        max_possible = ga.max_possible_average()
        min_possible = ga.min_possible_average()

        # Mesmo com todas as lacunas em 10, a meta não é atingível.
        if max_possible < target_average:
            raise CombinationNotFound()

        # Mesmo zerando as lacunas, a média já fica >= meta.
        already_achieved = min_possible >= target_average
        if already_achieved:
            solution = ga.zero_remaining_solution()
        else:
            solution, _, _ = ga.run()

            if solution is None:
                raise CombinationNotFound()

        n_current_tests = len(current_tests)
        n_current_assignments = len(current_assignments)
        test_weights = boletim.spec_test_weight or []
        assignment_weights = boletim.spec_assignment_weight or []

        # Resposta alinhada ao grade_optimizer: apenas lacunas (quero).
        boletim.provas = [
            {
                "valor": _round_grade_for_front(nota),
                "peso": _weight_for_front(test_weights[n_current_tests + i]),
            }
            for i, nota in enumerate(solution["tests"])
        ]
        boletim.trabalhos = [
            {
                "valor": _round_grade_for_front(nota),
                "peso": _weight_for_front(assignment_weights[n_current_assignments + i]),
            }
            for i, nota in enumerate(solution["assignments"])
        ]

        displayed_tests = current_tests + [item["valor"] for item in boletim.provas]
        displayed_assignments = current_assignments + [item["valor"] for item in boletim.trabalhos]
        final_avg = ga.calculate_weighted_average(
            displayed_tests,
            displayed_assignments,
            boletim.spec_test_weight,
            boletim.spec_assignment_weight,
        )

        boletim.target_avg = target_average
        boletim.final_avg = round(final_avg, 2)

        if already_achieved:
            boletim.status = "already_achieved"
            boletim.message = "Média desejada já atingida; lacunas preenchidas com 0"
            return boletim

        diff = abs(final_avg - target_average)
        if diff > CLOSE_DIFF_THRESHOLD:
            raise CombinationNotFound()

        if diff <= EXACT_DIFF_THRESHOLD:
            boletim.status = "exact"
            boletim.message = "O algoritmo retornou uma combinação válida de notas"
        else:
            boletim.status = "close"
            boletim.message = f"O algoritmo retornou uma solução próxima (diferença: {diff:.2f})"

        return boletim
