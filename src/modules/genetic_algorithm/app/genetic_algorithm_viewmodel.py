from src.shared.domain.entities.boletim_ga import Boletim_GA


class GeneticAlgorithmViewmodel:
    def __init__(self, boletim: Boletim_GA):
        self.boletim = boletim

    def to_dict(self) -> dict:
        return {
            "notas": {
                "provas": self.boletim.provas,
                "trabalhos": self.boletim.trabalhos,
            },
            "final_average": self.boletim.final_avg,
            "target_average": self.boletim.target_avg,
            "status": self.boletim.status,
            "message": self.boletim.message,
        }
