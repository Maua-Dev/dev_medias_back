import pytest

from src.shared.domain.entities.curso import Curso
from src.shared.infra.repositories.curso_repository_mock import CursoRepositoryMock


# Cada teste começa do zero: repositório novo, 
# com os mesmos cursos de exemplo, 
# para não misturar um teste com o outro.
@pytest.fixture
def repo() -> CursoRepositoryMock:
    return CursoRepositoryMock()


class TestCursoRepositoryMockGet:
    def test_get_curso_existente(self, repo: CursoRepositoryMock):
        c = repo.get_curso("ECM")
        assert c is not None
        assert c.código == "ECM"
        assert c.nome == "Engenharia de Computação"

    def test_get_curso_inexistente(self, repo: CursoRepositoryMock):
        assert repo.get_curso("NAO_EXISTE") is None


class TestCursoRepositoryMockGetAll:
    def test_get_all_cursos_tamanho_inicial(self, repo: CursoRepositoryMock):
        all_c = repo.get_all_cursos()
        assert len(all_c) == 3
        codigos = {c.código for c in all_c}
        assert codigos == {"ECM", "ADM", "CIC"}

    def test_get_all_cursos_retorno_nao_aliasing(self, repo: CursoRepositoryMock):
        first = repo.get_all_cursos()
        second = repo.get_all_cursos()
        assert first is not second
        assert first == second


class TestCursoRepositoryMockCreate:
    def test_create_curso_insere_e_retorna(self, repo: CursoRepositoryMock):
        novo = Curso(código="DIR", nome="Direito")
        out = repo.create_curso(novo)
        assert out is novo
        assert repo.get_curso("DIR") is novo
        assert len(repo.get_all_cursos()) == 4


class TestCursoRepositoryMockUpdate:
    def test_update_curso_put_substitui(self, repo: CursoRepositoryMock):
        atualizado = Curso(código="ECM", nome="Eng. de Computação (atualizado)")
        out = repo.update_curso(atualizado)
        assert out is atualizado
        loaded = repo.get_curso("ECM")
        assert loaded is not None
        assert loaded.nome == "Eng. de Computação (atualizado)"

    def test_update_curso_codigo_inexistente(self, repo: CursoRepositoryMock):
        assert repo.update_curso(Curso(código="X0", nome="Nome")) is None


class TestCursoRepositoryMockDelete:
    def test_delete_curso_remove_e_retorna(self, repo: CursoRepositoryMock):
        removed = repo.delete_curso("ADM")
        assert removed is not None
        assert removed.código == "ADM"
        assert repo.get_curso("ADM") is None
        assert len(repo.get_all_cursos()) == 2

    def test_delete_curso_inexistente(self, repo: CursoRepositoryMock):
        assert repo.delete_curso("NAO_EXISTE") is None
