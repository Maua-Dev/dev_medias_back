from typing import List, Optional

from src.shared.domain.entities.disciplina import Disciplina
from src.shared.domain.entities.disciplina import ItemAvaliacao
from src.shared.domain.repositories.disciplina_repository_interface import IDisciplinaRepository


class DisciplinaRepositoryMock(IDisciplinaRepository):

    def __init__(self):
        self.disciplinas = [
            Disciplina(
                code="ECM101",
                name="Engenharia de Computação",
                course="ECM",
                period="2024.1",
                exam_weight=0.6,
                assignment_weight=0.4,
                exams=[ItemAvaliacao(name="P1", weight=0.6)],
                assignments=[ItemAvaliacao(name="T1", weight=0.4)],
                courses={"ECM": 4},
            ),
            Disciplina(
                code="ECM102",
                name="Engenharia de Software",
                course="ECM",
                period="2024.1",
                exam_weight=0.6,
                assignment_weight=0.4,
                exams=[ItemAvaliacao(name="P1", weight=0.6)],
                assignments=[ItemAvaliacao(name="T1", weight=0.4)],
                courses={"ECM": 3},
            ),
            Disciplina(
                code="ECM103",
                name="Arquitetura de Computadores",
                course="ECM",
                period="2024.1",
                exam_weight=0.6,
                assignment_weight=0.4,
                exams=[ItemAvaliacao(name="P1", weight=0.6)],
                assignments=[ItemAvaliacao(name="T1", weight=0.4)],
                courses={"ECM": 2},
            ),
            Disciplina(
                code="ECM104",
                name="Algoritmos e Estruturas de Dados",
                course="ECM",
                period="2024.1",
                exam_weight=0.6,
                assignment_weight=0.4,
                exams=[ItemAvaliacao(name="P1", weight=0.6)],
                assignments=[ItemAvaliacao(name="T1", weight=0.4)],
                courses={"ECM": 1},
            ),
        ]

    def create_disciplina(self, disciplina: Disciplina) -> Optional[Disciplina]:
        self.disciplinas.append(disciplina)
        return disciplina

    def get_disciplina(self, code: str) -> Optional[Disciplina]:
        return next((d for d in self.disciplinas if d.code == code), None)

    def update_disciplina(self, disciplina: Disciplina) -> Optional[Disciplina]:
        for i, d in enumerate(self.disciplinas):
            if d.code == disciplina.code:
                self.disciplinas[i] = disciplina
                return disciplina
        return None

    def delete_disciplina(self, code: str) -> Optional[Disciplina]:
        for i, d in enumerate(self.disciplinas):
            if d.code == code:
                return self.disciplinas.pop(i)
        return None

    def get_all_disciplinas(self) -> List[Disciplina]:
        return list(self.disciplinas)
