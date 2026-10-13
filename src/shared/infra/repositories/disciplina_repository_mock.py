from copy import deepcopy
from typing import List, Optional

from src.shared.domain.entities.disciplina import Disciplina, ItemAvaliacao
from src.shared.domain.repositories.disciplina_repository_interface import IDisciplinaRepository
from src.shared.infra.external.dynamo.academic_catalog.single_table_keys import (
    GLOBAL_OWNER,
    normalize_owner_id,
)


def _seed_catalog() -> list[Disciplina]:
    return [
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
            is_custom=False,
            device_id=None,
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
            is_custom=False,
            device_id=None,
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
            is_custom=False,
            device_id=None,
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
            is_custom=False,
            device_id=None,
        ),
    ]


class DisciplinaRepositoryMock(IDisciplinaRepository):
    """In-memory repo scoped by owner (GLOBAL catalog or device_id)."""

    _STORE: dict[str, list[Disciplina]] | None = None

    def __init__(self, user_id: Optional[str] = None):
        self._owner = normalize_owner_id(user_id)
        if DisciplinaRepositoryMock._STORE is None:
            DisciplinaRepositoryMock._STORE = {GLOBAL_OWNER: _seed_catalog()}
        if self._owner not in DisciplinaRepositoryMock._STORE:
            DisciplinaRepositoryMock._STORE[self._owner] = []

    @classmethod
    def reset_store(cls) -> None:
        cls._STORE = {GLOBAL_OWNER: _seed_catalog()}

    @property
    def disciplinas(self) -> list[Disciplina]:
        assert self._STORE is not None
        return self._STORE[self._owner]

    @disciplinas.setter
    def disciplinas(self, value: list[Disciplina]) -> None:
        assert self._STORE is not None
        self._STORE[self._owner] = value

    def create_disciplina(self, disciplina: Disciplina) -> Optional[Disciplina]:
        stored = deepcopy(disciplina)
        self.disciplinas.append(stored)
        return deepcopy(stored)

    def get_disciplina(self, code: str) -> Optional[Disciplina]:
        found = next((d for d in self.disciplinas if d.code == code), None)
        return deepcopy(found) if found else None

    def update_disciplina(self, disciplina: Disciplina) -> Optional[Disciplina]:
        for index, current in enumerate(self.disciplinas):
            if current.code == disciplina.code:
                stored = deepcopy(disciplina)
                self.disciplinas[index] = stored
                return deepcopy(stored)
        return None

    def delete_disciplina(self, code: str) -> Optional[Disciplina]:
        for index, current in enumerate(self.disciplinas):
            if current.code == code:
                removed = self.disciplinas.pop(index)
                return deepcopy(removed)
        return None

    def get_all_disciplinas(self) -> List[Disciplina]:
        return [deepcopy(item) for item in self.disciplinas]
