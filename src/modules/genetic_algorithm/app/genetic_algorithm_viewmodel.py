from src.shared.domain.entities.boletim_ga import Boletim_GA
from src.shared.domain.entities.nota import Nota



class GeneticAlgorithmViewmodel:
    boletim: Boletim_GA

    def __init__(self, boletim: Boletim_GA):
        self.boletim = boletim

    def to_dict(self)-> dict:
        all_tests = self.boletim.current_tests + self.boletim.calculated_tests
        all_assignments = self.boletim.current_assignments + self.boletim.calculated_assignments

        provas = []
        for i, grade in enumerate(all_tests):
            prova = {
                "nota": round(grade, 2),
                "peso": round(self.boletim.spec_test_weight[i], 2) if self.boletim.spec_test_weight else None
            }
            provas.append(prova)


        trabalhos = []
        for i, grade in enumerate(all_assignments):
            trabalho = {
                "nota": round(grade, 2),
                "peso": round(self.boletim.spec_assignment_weight[i], 2) if self.boletim.spec_assignment_weight else None
            }
            trabalhos.append(trabalho)

        final_avg = self.calculate_weighted_average(
            all_tests,
            all_assignments,
            self.boletim.spec_test_weight,
            self.boletim.spec_assignment_weight
        )

        diff = abs(final_avg - self.boletim.target_avg)

        if diff <= 0.05:
                message = "O algoritmo retornou uma combinação válida de notas"
        elif diff <=0.2:
                message = f"O algoritmo retornou uma solução próxima (diferença: {diff:.2f})"
        else:
                message = f"O algoritmo não conseguiu encontrar uma solução próxima (diferença: {diff:.2f})"
        
        response = {
            "notas":{
                "peso provas": round(self.boletim.test_weight,2),
                "provas": provas,
                "peso trabalhos": round(self.boletim.assignment_weight,2),
                "trabalhos": trabalhos
            },
            "message": message
        }
        return response
