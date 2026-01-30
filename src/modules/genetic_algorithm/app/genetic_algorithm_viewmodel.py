from src.shared.domain.entities import boletim
from src.shared.domain.entities.boletim_ga import Boletim_GA
from src.shared.domain.entities.nota import Nota



class GeneticAlgorithmViewmodel:
    

    def __init__(self, body: dict):
        self.body = body
    
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
        total_tests = len(self.body['current_tests']) + self.body['num_remaining_tests']
        total_assignments = len(self.body['current_assignments']) + self.body['num_remaining_assignments']

        # Só tem trabalhos
        if total_tests == 0:
            return assignment_avg
        
        # Só tem provas
        if total_assignments == 0:
            return test_avg

        
        # ===== MÉDIA PONDERADA ENTRE PROVAS E TRABALHOS =====
        return (test_avg * self.body['test_weight']) + (assignment_avg * self.body['assignment_weight'])

    def to_dict(self)-> dict:
       
        all_tests = self.body['current_tests'] + self.body['tests']
        all_assignments = self.body['current_assignments'] + self.body['assignments']
        
        provas = []
        for i, grade in enumerate(all_tests):
            prova = {
                "nota": round(grade, 2),
                "peso": round(self.body['spec_test_weight'][i], 2) if self.body['spec_test_weight'] else None
            }
            provas.append(prova)


        trabalhos = []
        for i, grade in enumerate(all_assignments):
            trabalho = {
                "nota": round(grade, 2),
                "peso": round(self.body['spec_assignment_weight'][i], 2) if self.body['spec_assignment_weight'] else None
            }
            trabalhos.append(trabalho)

        final_avg = self.calculate_weighted_average(
            all_tests,
            all_assignments,
            self.body['spec_test_weight'],
            self.body['spec_assignment_weight']
        )

        diff = abs(final_avg - self.body['target_average'])

        if diff <= 0.05:
                message = "O algoritmo retornou uma combinação válida de notas"
        elif diff <=0.2:
                message = f"O algoritmo retornou uma solução próxima (diferença: {diff:.2f})"
        else:
                message = f"O algoritmo não conseguiu encontrar uma solução próxima (diferença: {diff:.2f})"
        
        response = {
            "notas":{
                "peso provas": round(self.body['test_weight'],2),
                "provas": provas,
                "peso trabalhos": round(self.body['assignment_weight'],2),
                "trabalhos": trabalhos
            },
            "final_average": round(final_avg,2),
            "message": message
        }
        return response
