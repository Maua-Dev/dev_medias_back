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

         # Desempacota atributos do boletim
        current_tests = boletim.current_tests
        current_assignments = boletim.current_assignments
        num_remaining_tests = boletim.num_remaining_tests
        num_remaining_assignments = boletim.num_remaining_assignments
        test_weight = boletim.test_weight
        assignment_weight = boletim.assignment_weight
        spec_test_weight = boletim.spec_test_weight
        spec_assignment_weight = boletim.spec_assignment_weight

        # Agora atribui aos self
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

    def create_individual(self):
        """Cria um indivíduo (notas futuras de testes e trabalhos)"""
        tests = [random.uniform(0, self.max_grade) for _ in range(self.num_remaining_tests)]
        assignments = [random.uniform(0, self.max_grade) for _ in range(self.num_remaining_assignments)]
        return {'tests': tests, 'assignments': assignments}

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

        # ===== CALCULA MÉDIA DAS PROVAS =====
        if tests:
            if spec_test_weight is not None:
                # Média ponderada (NÃO modifica lista original)
                tests_weighted = [tests[i] * spec_test_weight[i] for i in range(len(tests))]
                test_avg = sum(tests_weighted) / sum(spec_test_weight)
            else:
                # Média simples
                test_avg = sum(tests) / len(tests)
        else:
            test_avg = 0

        # ===== CALCULA MÉDIA DOS TRABALHOS =====
        if assignments:
            if spec_assignment_weight is not None:
                # Média ponderada (NÃO modifica lista original)
                assignments_weighted = [assignments[i] * spec_assignment_weight[i] for i in range(len(assignments))]
                assignment_avg = sum(assignments_weighted) / sum(spec_assignment_weight)
            else:
                # Média simples
                assignment_avg = sum(assignments) / len(assignments)
        else:
            assignment_avg = 0

        # ===== VERIFICA CASOS ESPECIAIS =====
        total_tests = len(self.current_tests) + self.num_remaining_tests
        total_assignments = len(self.current_assignments) + self.num_remaining_assignments

        # Só tem trabalhos
        if total_tests == 0:
            return assignment_avg
        
        # Só tem provas
        if total_assignments == 0:
            return test_avg

        
        # ===== MÉDIA PONDERADA ENTRE PROVAS E TRABALHOS =====
        return (test_avg * self.test_weight) + (assignment_avg * self.assignment_weight)

    def fitness(self, individual):
        """
        Função fitness que minimiza:
        1. Diferença da média alvo
        2. Variância entre as notas (para mantê-las similares)
        """
        all_tests = self.current_tests + individual['tests']
        all_assignments = self.current_assignments + individual['assignments']

        # IMPORTANTE: Passa os 4 parâmetros
        avg = self.calculate_weighted_average(
            all_tests, 
            all_assignments,
            self.spec_test_weight,
            self.spec_assignment_weight
        )

        # Penalidade por não atingir a média
        avg_diff = abs(avg - self.target_avg)

        # Penalidade por variância (queremos notas equilibradas)
        future_grades = individual['tests'] + individual['assignments']
        variance_penalty = np.std(future_grades) if len(future_grades) > 1 else 0

        # Penalidade por notas impossíveis
        impossible_penalty = sum(max(0, g - self.max_grade) for g in future_grades)

        return avg_diff * 10 + variance_penalty * 2 + impossible_penalty * 20

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

            # Crossover testes
            if self.num_remaining_tests > 0:
                point = random.randint(0, len(parent1['tests']))
                child1['tests'] = parent1['tests'][:point] + parent2['tests'][point:]
                child2['tests'] = parent2['tests'][:point] + parent1['tests'][point:]

            # Crossover trabalhos
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
        """Mutação gaussiana"""
        mutated = {
            'tests': individual['tests'].copy(),
            'assignments': individual['assignments'].copy()
        }

        for i in range(len(mutated['tests'])):
            if random.random() < 0.2:
                mutated['tests'][i] += random.gauss(0, 0.5)
                mutated['tests'][i] = max(0, min(self.max_grade, mutated['tests'][i]))

        for i in range(len(mutated['assignments'])):
            if random.random() < 0.2:
                mutated['assignments'][i] += random.gauss(0, 0.5)
                mutated['assignments'][i] = max(0, min(self.max_grade, mutated['assignments'][i]))

        return mutated

    def run(self):
        """Executa o algoritmo genético. Retorna a melhor solução encontrada e seu respectivo fitness."""
        population = [self.create_individual() for _ in range(self.pop_size)]

        best_ever = None
        best_fitness_ever = float('inf')

        for gen in range(self.generations):
            fitnesses = [self.fitness(ind) for ind in population]

            min_idx = fitnesses.index(min(fitnesses))
            if fitnesses[min_idx] < best_fitness_ever:
                best_fitness_ever = fitnesses[min_idx]
                best_ever = {
                    'tests': population[min_idx]['tests'].copy(),
                    'assignments': population[min_idx]['assignments'].copy()
                }

            new_population = []

            # Elitismo
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

            if gen % 100 == 0:
                print(f"Geração {gen}: Melhor fitness = {best_fitness_ever:.4f}")


        return best_ever, best_fitness_ever

    def display_results(self, solution):
        """Exibe os resultados"""
        all_tests = self.current_tests + solution['tests']
        all_assignments = self.current_assignments + solution['assignments']

        # IMPORTANTE: Passa os 4 parâmetros
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



    def get_results_json(self,solution):
        all_tests = self.current_tests + solution['tests']
        all_assignments = self.current_assignments + solution['assignments']
        
        provas = []
        for i, grade in enumerate(all_tests):
            prova = {
                "nota": round(grade, 2),
                "peso": round(self.spec_test_weight[i], 2) if self.spec_test_weight else None
            }
            provas.append(prova)


        trabalhos = []
        for i, grade in enumerate(all_assignments):
            trabalho = {
                "nota": round(grade, 2),
                "peso": round(self.spec_assignment_weight[i], 2) if self.spec_assignment_weight else None
            }
            trabalhos.append(trabalho)

        final_avg = self.calculate_weighted_average(
            all_tests,
            all_assignments,
            self.spec_test_weight,
            self.spec_assignment_weight
        )

        diff = abs(final_avg - self.target_avg)

        if diff <= 0.05:
                message = "O algoritmo retornou uma combinação válida de notas"
        elif diff <=0.2:
                message = f"O algoritmo retornou uma solução próxima (diferença: {diff:.2f})"
        else:
                message = f"O algoritmo não conseguiu encontrar uma solução próxima (diferença: {diff:.2f})"
        
        response = {
            "notas":{
                "peso provas": round(self.test_weight,2),
                "provas": provas,
                "peso trabalhos": round(self.assignment_weight,2),
                "trabalhos": trabalhos
            },
            "final_average": round(final_avg,2),
            "message": message
        }
        return response