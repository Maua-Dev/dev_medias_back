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
            "message": self.boletim.message,
        }
    
        
    
