from src.shared.domain.entities.boletim_ga import Boletim_GA
import random
import numpy as np
from typing import Optional


class GradeGeneticAlgorithm:

    def __init__(
        self,
        boletim: Boletim_GA,
        target_average: float,
        max_grade: float = 10.0,
        population_size: int = 150,
        generations: int = 200,
        final_avg: float = 0.0
    ) -> None:

        current_tests = boletim.current_tests
        current_assignments = boletim.current_assignments
        num_remaining_tests = boletim.num_remaining_tests
        num_remaining_assignments = boletim.num_remaining_assignments
        test_weight = boletim.test_weight
        assignment_weight = boletim.assignment_weight
        spec_test_weight = boletim.spec_test_weight
        spec_assignment_weight = boletim.spec_assignment_weight

        self.current_tests: list[float] = current_tests
        self.current_assignments: list[float] = current_assignments
        self.num_remaining_tests: int = num_remaining_tests
        self.num_remaining_assignments: int = num_remaining_assignments
        self.test_weight: float = test_weight
        self.assignment_weight: float = assignment_weight
        self.spec_test_weight: Optional[list[float]] = spec_test_weight
        self.spec_assignment_weight: Optional[list[float]] = spec_assignment_weight
        self.target_avg: float = target_average
        self.max_grade: float = max_grade
        self.pop_size: int = population_size
        self.generations: int = generations
        self.grade_domain: list[float] = [
            i / 2.0 for i in range(int(self.max_grade * 2) + 1)
        ]

    def _random_grade(self) -> float:
        """Nota aleatória no domínio Mauá {0, 0.5, ..., max_grade}."""
        return random.choice(self.grade_domain)

    def _snap_to_domain(self, grade: float) -> float:
        snapped = round(grade * 2) / 2.0
        return max(0.0, min(self.max_grade, snapped))

    def create_individual(self):
        """Cria um indivíduo (notas futuras de testes e trabalhos) no domínio 0.5."""
        tests = [self._random_grade() for _ in range(self.num_remaining_tests)]
        assignments = [self._random_grade() for _ in range(self.num_remaining_assignments)]
        return {'tests': tests, 'assignments': assignments}

    def _average_with_remaining(self, remaining_grade: float) -> float:
        """Média final preenchendo todas as lacunas com o mesmo valor."""
        tests = self.current_tests + [remaining_grade] * self.num_remaining_tests
        assignments = self.current_assignments + [remaining_grade] * self.num_remaining_assignments
        return self.calculate_weighted_average(
            tests,
            assignments,
            self.spec_test_weight,
            self.spec_assignment_weight,
        )

    def max_possible_average(self) -> float:
        """Maior média possível (todas as lacunas = nota máxima)."""
        return self._average_with_remaining(self.max_grade)

    def min_possible_average(self) -> float:
        """Menor média possível (todas as lacunas = 0)."""
        return self._average_with_remaining(0.0)

    def zero_remaining_solution(self) -> dict:
        """Solução com lacunas zeradas (meta já garantida)."""
        return {
            'tests': [0.0] * self.num_remaining_tests,
            'assignments': [0.0] * self.num_remaining_assignments,
        }

    def calculate_weighted_average(self, tests, assignments, spec_test_weight=None, spec_assignment_weight=None):
        """
        Calcula média ponderada com suporte a pesos específicos opcionais.

        Lógica:
        1. Se spec_test_weight fornecido: média ponderada das provas
        2. Senão: média simples das provas
        3. Se spec_assignment_weight fornecido: média ponderada dos trabalhos
        4. Senão: média simples dos trabalhos
        5. Combina médias com test_weight e assignment_weight
        """
        if not tests and not assignments:
            return 0

        if tests:
            if spec_test_weight is not None:
                tests_weighted = [tests[i] * spec_test_weight[i] for i in range(len(tests))]
                test_avg = sum(tests_weighted) / sum(spec_test_weight)
            else:
                test_avg = sum(tests) / len(tests)
        else:
            test_avg = 0

        if assignments:
            if spec_assignment_weight is not None:
                assignments_weighted = [assignments[i] * spec_assignment_weight[i] for i in range(len(assignments))]
                assignment_avg = sum(assignments_weighted) / sum(spec_assignment_weight)
            else:
                assignment_avg = sum(assignments) / len(assignments)
        else:
            assignment_avg = 0

        total_tests = len(self.current_tests) + self.num_remaining_tests
        total_assignments = len(self.current_assignments) + self.num_remaining_assignments

        if total_tests == 0:
            return assignment_avg

        if total_assignments == 0:
            return test_avg

        return (test_avg * self.test_weight) + (assignment_avg * self.assignment_weight)

    def fitness(self, individual):
        """
        Minimiza primeiro a distância da meta (prioridade absoluta),
        depois a variância das lacunas (apenas desempate).
        Undershoot é penalizado mais que overshoot.
        """
        all_tests = self.current_tests + individual['tests']
        all_assignments = self.current_assignments + individual['assignments']

        avg = self.calculate_weighted_average(
            all_tests,
            all_assignments,
            self.spec_test_weight,
            self.spec_assignment_weight
        )

        avg_diff = abs(avg - self.target_avg)
        undershoot = max(0.0, self.target_avg - avg)

        future_grades = individual['tests'] + individual['assignments']
        variance_penalty = np.std(future_grades) if len(future_grades) > 1 else 0.0
        impossible_penalty = sum(max(0, g - self.max_grade) for g in future_grades)

        # avg_diff domina; variância só desempatada soluções altamente próximas da meta
        return (
            avg_diff * 1000.0
            + undershoot * 500.0
            + variance_penalty * 0.1
            + impossible_penalty * 20.0
        )

    def selection(self, population, fitnesses):
        """Seleção por torneio"""
        tournament_size = 3
        tournament = random.sample(list(zip(population, fitnesses)), tournament_size)
        tournament.sort(key=lambda x: x[1])
        return tournament[0][0], tournament[1][0]

    def crossover(self, parent1, parent2):
        """Crossover separado para testes e trabalhos"""
        if random.random() < 0.8:
            child1 = {'tests': [], 'assignments': []}
            child2 = {'tests': [], 'assignments': []}

            if self.num_remaining_tests > 0:
                point = random.randint(0, len(parent1['tests']))
                child1['tests'] = parent1['tests'][:point] + parent2['tests'][point:]
                child2['tests'] = parent2['tests'][:point] + parent1['tests'][point:]

            if self.num_remaining_assignments > 0:
                point = random.randint(0, len(parent1['assignments']))
                child1['assignments'] = parent1['assignments'][:point] + parent2['assignments'][point:]
                child2['assignments'] = parent2['assignments'][:point] + parent1['assignments'][point:]

            return child1, child2

        return {
            'tests': parent1['tests'].copy(),
            'assignments': parent1['assignments'].copy()
        }, {
            'tests': parent2['tests'].copy(),
            'assignments': parent2['assignments'].copy()
        }

    def mutate(self, individual):
        """Mutação em passos de 0.5 no domínio Mauá."""
        mutated = {
            'tests': individual['tests'].copy(),
            'assignments': individual['assignments'].copy()
        }

        for i in range(len(mutated['tests'])):
            if random.random() < 0.2:
                step = random.choice([-1.0, 1.0]) * 0.5
                mutated['tests'][i] = self._snap_to_domain(mutated['tests'][i] + step)

        for i in range(len(mutated['assignments'])):
            if random.random() < 0.2:
                step = random.choice([-1.0, 1.0]) * 0.5
                mutated['assignments'][i] = self._snap_to_domain(mutated['assignments'][i] + step)

        return mutated

    def run(self):
        """Executa o algoritmo genético. Retorna a melhor solução encontrada e seu respectivo fitness."""
        population = [self.create_individual() for _ in range(self.pop_size)]

        best_ever = None
        best_fitness_ever = float('inf')

        for _ in range(self.generations):
            fitnesses = [self.fitness(ind) for ind in population]

            min_idx = fitnesses.index(min(fitnesses))
            if fitnesses[min_idx] < best_fitness_ever:
                best_fitness_ever = fitnesses[min_idx]
                best_ever = {
                    'tests': population[min_idx]['tests'].copy(),
                    'assignments': population[min_idx]['assignments'].copy()
                }

            new_population = []

            sorted_pop = sorted(zip(population, fitnesses), key=lambda x: x[1])
            new_population.extend([
                {'tests': ind['tests'].copy(), 'assignments': ind['assignments'].copy()}
                for ind, _ in sorted_pop[:2]
            ])

            while len(new_population) < self.pop_size:
                p1, p2 = self.selection(population, fitnesses)
                c1, c2 = self.crossover(p1, p2)
                c1 = self.mutate(c1)
                c2 = self.mutate(c2)
                new_population.extend([c1, c2])

            population = new_population[:self.pop_size]

        final_avg = self.calculate_weighted_average(
            self.current_tests + best_ever['tests'],
            self.current_assignments + best_ever['assignments'],
            self.spec_test_weight,
            self.spec_assignment_weight,
        )

        return best_ever, best_fitness_ever, final_avg

    def display_results(self, solution):
        """Exibe os resultados (uso local/debug)."""
        all_tests = self.current_tests + solution['tests']
        all_assignments = self.current_assignments + solution['assignments']

        current_avg = self.calculate_weighted_average(
            self.current_tests,
            self.current_assignments,
            self.spec_test_weight,
            self.spec_assignment_weight
        )

        final_avg = self.calculate_weighted_average(
            all_tests,
            all_assignments,
            self.spec_test_weight,
            self.spec_assignment_weight
        )

        print("\n" + "="*60)
        print("RESULTADOS")
        print("="*60)
        print(f"Pesos: Provas {self.test_weight*100:.0f}% | Trabalhos {self.assignment_weight*100:.0f}%")

        if self.spec_test_weight is not None:
            print(f"Pesos específicos de provas: {[f'{w*100:.0f}%' for w in self.spec_test_weight]}")
        if self.spec_assignment_weight is not None:
            print(f"Pesos específicos de trabalhos: {[f'{w*100:.0f}%' for w in self.spec_assignment_weight]}")

        print(f"\nProvas atuais: {[f'{g:.2f}' for g in self.current_tests]}")
        print(f"Trabalhos atuais: {[f'{g:.2f}' for g in self.current_assignments]}")

        if solution['tests']:
            print(f"\nProvas necessárias:")
            for i, grade in enumerate(solution['tests'], 1):
                print(f"  Prova {i}: {grade:.2f}")

        if solution['assignments']:
            print(f"\nTrabalhos necessários:")
            for i, grade in enumerate(solution['assignments'], 1):
                print(f"  Trabalho {i}: {grade:.2f}")

        print(f"\nMédia atual: {current_avg:.2f}")
        print(f"Média alvo: {self.target_avg:.2f}")
        print(f"Média final prevista: {final_avg:.2f}")

        future_grades = solution['tests'] + solution['assignments']
        if len(future_grades) > 1:
            print(f"Desvio padrão das notas futuras: {np.std(future_grades):.2f}")
        print("="*60)

        return final_avg

    def get_results_json(self, solution):
        remaining_tests = solution['tests']
        remaining_assignments = solution['assignments']
        n_current_tests = len(self.current_tests)
        n_current_assignments = len(self.current_assignments)

        provas = []
        for i, grade in enumerate(remaining_tests):
            weight_idx = n_current_tests + i
            prova = {
                "nota": round(grade, 2),
                "peso": round(self.spec_test_weight[weight_idx], 4) if self.spec_test_weight else None
            }
            provas.append(prova)

        trabalhos = []
        for i, grade in enumerate(remaining_assignments):
            weight_idx = n_current_assignments + i
            trabalho = {
                "nota": round(grade, 2),
                "peso": round(self.spec_assignment_weight[weight_idx], 4) if self.spec_assignment_weight else None
            }
            trabalhos.append(trabalho)

        final_avg = self.calculate_weighted_average(
            self.current_tests + remaining_tests,
            self.current_assignments + remaining_assignments,
            self.spec_test_weight,
            self.spec_assignment_weight
        )

        diff = abs(final_avg - self.target_avg)

        if diff <= 0.05:
            message = "O algoritmo retornou uma combinação válida de notas"
        elif diff <= 0.2:
            message = f"O algoritmo retornou uma solução próxima (diferença: {diff:.2f})"
        else:
            message = f"O algoritmo não conseguiu encontrar uma solução próxima (diferença: {diff:.2f})"

        return {
            "notas": {
                "provas": provas,
                "trabalhos": trabalhos
            },
            "final_average": round(final_avg, 2),
            "message": message
        }
