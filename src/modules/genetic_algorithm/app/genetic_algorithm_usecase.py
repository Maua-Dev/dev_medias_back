from src.shared.domain.entities.boletim_ga import Boletim_GA
from src.shared.helpers.errors.usecase_errors import CombinationNotFound
from src.shared.genetic_algorithm_solver import GradeGeneticAlgorithm


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

        solution, fitness, final_avg = ga.run()

        if solution is None:
            raise CombinationNotFound()

        all_tests = current_tests + solution["tests"]
        all_assignments = current_assignments + solution["assignments"]

        boletim.target_avg = target_average
        boletim.final_avg = final_avg
        boletim.provas = [
            {"valor": round(nota, 2), "peso": round(boletim.spec_test_weight[i], 2)}
            for i, nota in enumerate(all_tests)
        ]
        boletim.trabalhos = [
            {"valor": round(nota, 2), "peso": round(boletim.spec_assignment_weight[i], 2)}
            for i, nota in enumerate(all_assignments)
        ]

        diff = abs(final_avg - target_average)
        if diff <= 0.05:
            boletim.message = "O algoritmo retornou uma combinação válida de notas"
        elif diff <= 0.2:
            boletim.message = f"O algoritmo retornou uma solução próxima (diferença: {diff:.2f})"
        else:
            boletim.message = f"O algoritmo não conseguiu encontrar uma solução próxima (diferença: {diff:.2f})"

        return boletim
        