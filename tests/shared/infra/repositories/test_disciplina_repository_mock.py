import pytest

from src.shared.domain.entities.disciplina import Disciplina, ItemAvaliacao
from src.shared.infra.repositories.disciplina_repository_mock import DisciplinaRepositoryMock


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


@pytest.fixture(autouse=True)
def _reset_store():
    DisciplinaRepositoryMock.reset_store()
    yield
    DisciplinaRepositoryMock.reset_store()


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
        assert out is not None
        assert out.code == nova.code
        assert repo.get_disciplina("ECM999") is not None
        assert len(repo.get_all_disciplinas()) == 5


class TestDisciplinaRepositoryMockUpdate:
    def test_update_disciplina_put_substitui(self, repo: DisciplinaRepositoryMock):
        atualizada = _disciplina("ECM101", name="Nome atualizado")
        out = repo.update_disciplina(atualizada)
        assert out is not None
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


class TestDisciplinaRepositoryMockOwnerScope:
    def test_device_partition_isolated(self):
        device = "550e8400-e29b-41d4-a716-446655440000"
        device_repo = DisciplinaRepositoryMock(user_id=device)
        device_repo.create_disciplina(
            _disciplina("MIN001").model_copy(update={"device_id": device, "is_custom": True})
        )
        assert device_repo.get_disciplina("MIN001") is not None
        assert DisciplinaRepositoryMock().get_disciplina("MIN001") is None
        assert DisciplinaRepositoryMock(user_id=device).get_disciplina("ECM101") is None
