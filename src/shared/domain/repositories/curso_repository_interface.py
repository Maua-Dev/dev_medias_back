from abc import ABC, abstractmethod
from typing import List, Optional

from src.shared.domain.entities.curso import Curso


class ICursoRepository(ABC):

    @abstractmethod
    def create_curso(self, curso: Curso) -> Optional[Curso]:
        """
        Persiste o curso e retorna a entidade salva.
        """
        pass

    @abstractmethod
    def get_curso(self, código: str) -> Optional[Curso]:
        """
        Retorna o curso pelo código, ou None se não existir.
        """
        pass

    @abstractmethod
    def update_curso(self, curso: Curso) -> Optional[Curso]:
        """
        Substitui integralmente o curso identificado por `curso.código` (PUT).
        Retorna a entidade atualizada, ou None se não existir registro com esse código.
        """
        pass

    @abstractmethod
    def delete_curso(self, código: str) -> Optional[Curso]:
        """
        Remove o curso pelo código e retorna a entidade removida, ou None.
        """
        pass

    @abstractmethod
    def get_all_cursos(self) -> List[Curso]:
        """
        Retorna todos os cursos persistidos.
        """
        pass
