from abc import ABC, abstractmethod
from typing import List, Optional

from src.shared.domain.entities.disciplina import Disciplina


class IDisciplinaRepository(ABC):

    @abstractmethod
    def create_disciplina(self, disciplina: Disciplina) -> Optional[Disciplina]:
        """
        Persiste a disciplina e retorna a entidade salva.
        """
        pass

    @abstractmethod
    def get_disciplina(self, code: str) -> Optional[Disciplina]:
        """
        Retorna a disciplina pelo código, ou None se não existir.
        """
        pass

    @abstractmethod
    def update_disciplina(self, disciplina: Disciplina) -> Optional[Disciplina]:
        """
        Substitui integralmente a disciplina identificada por `disciplina.code` (PUT).
        Retorna a entidade atualizada, ou None se não existir registro com esse código.
        """
        pass

    @abstractmethod
    def delete_disciplina(self, code: str) -> Optional[Disciplina]:
        """
        Remove a disciplina pelo código e retorna a entidade removida, ou None.
        """
        pass

    @abstractmethod
    def get_all_disciplinas(self) -> List[Disciplina]:
        """
        Retorna todas as disciplinas persistidas.
        """
        pass
