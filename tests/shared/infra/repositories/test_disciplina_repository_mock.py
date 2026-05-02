import pytest

from src.shared.domain.entities.disciplina import Disciplina, ItemAvaliacao
from src.shared.infra.repositories.disciplina_repository_mock import DisciplinaRepositoryMock

# Função auxiliar para criar uma disciplina com valores padrão.
def _disciplina(code: str, *, name: str = "Nome") -> Disciplina:
    return Disciplina(
        course="ECM",
        name=name,
        code=code,
        period="2024.1",
        exam_weight=0.5,
        assignment_weight=0.5,
        exams=[ItemAvaliacao(name="P1", weight=0.5)],
        assignments=[ItemAvaliacao(name="T1", weight=0.5)],
        courses={"ECM": 1},
    )


# Cada teste começa do zero: repositório novo, 
# com as mesmas disciplinas de exemplo, 
# para não misturar um teste com outro.
@pytest.fixture
def repo() -> DisciplinaRepositoryMock:
    return DisciplinaRepositoryMock()


class TestDisciplinaRepositoryMockGet:
    def test_get_disciplina_existente(self, repo: DisciplinaRepositoryMock):
        d = repo.get_disciplina("ECM101")
        assert d is not None
        assert d.code == "ECM101"
        assert d.name == "Engenharia de Computação"

    def test_get_disciplina_inexistente(self, repo: DisciplinaRepositoryMock):
        assert repo.get_disciplina("NAO_EXISTE") is None


class TestDisciplinaRepositoryMockGetAll:
    def test_get_all_disciplinas_tamanho_inicial(self, repo: DisciplinaRepositoryMock):
        all_d = repo.get_all_disciplinas()
        assert len(all_d) == 4
        codes = {d.code for d in all_d}
        assert codes == {"ECM101", "ECM102", "ECM103", "ECM104"}

    def test_get_all_disciplinas_retorno_nao_aliasing(
        self, repo: DisciplinaRepositoryMock
    ):
        first = repo.get_all_disciplinas()
        second = repo.get_all_disciplinas()
        assert first is not second
        assert first == second


class TestDisciplinaRepositoryMockCreate:
    def test_create_disciplina_insere_e_retorna(self, repo: DisciplinaRepositoryMock):
        nova = _disciplina("ECM999", name="Nova")
        out = repo.create_disciplina(nova)
        assert out is nova
        assert repo.get_disciplina("ECM999") is nova
        assert len(repo.get_all_disciplinas()) == 5


class TestDisciplinaRepositoryMockUpdate:
    def test_update_disciplina_put_substitui(self, repo: DisciplinaRepositoryMock):
        atualizada = _disciplina("ECM101", name="Nome atualizado")
        out = repo.update_disciplina(atualizada)
        assert out is atualizada
        loaded = repo.get_disciplina("ECM101")
        assert loaded is not None
        assert loaded.name == "Nome atualizado"

    def test_update_disciplina_codigo_inexistente(self, repo: DisciplinaRepositoryMock):
        assert repo.update_disciplina(_disciplina("X0")) is None


class TestDisciplinaRepositoryMockDelete:
    def test_delete_disciplina_remove_e_retorna(self, repo: DisciplinaRepositoryMock):
        removed = repo.delete_disciplina("ECM102")
        assert removed is not None
        assert removed.code == "ECM102"
        assert repo.get_disciplina("ECM102") is None
        assert len(repo.get_all_disciplinas()) == 3

    def test_delete_disciplina_inexistente(self, repo: DisciplinaRepositoryMock):
        assert repo.delete_disciplina("NAO_EXISTE") is None
