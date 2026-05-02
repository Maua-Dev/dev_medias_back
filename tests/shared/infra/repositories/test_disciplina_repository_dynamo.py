import os
import socket
import uuid

import pytest

pytest.importorskip("boto3")

from src.shared.domain.entities.disciplina import Disciplina, ItemAvaliacao
from src.shared.infra.repositories.disciplina_repository_dynamo import DisciplinaRepositoryDynamo
from src.shared.infra.repositories.disciplina_repository_mock import DisciplinaRepositoryMock


def _configure_test_env() -> None:
    os.environ["STAGE"] = "TEST"
    port = os.environ.get("DYNAMO_HOST_PORT", "8000")
    os.environ.setdefault("ENDPOINT_URL", f"http://127.0.0.1:{port}")
    os.environ.setdefault("ACADEMIC_CATALOG_TABLE_NAME", "DevMediasAcademicCatalogTable-test")


def _unique_code(prefix: str = "DYN") -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12].upper()}"


def _clone_with_code(source: Disciplina, code: str) -> Disciplina:
    return Disciplina(
        course=source.course,
        name=source.name,
        code=code,
        period=source.period,
        exam_weight=source.exam_weight,
        assignment_weight=source.assignment_weight,
        exams=list(source.exams),
        assignments=list(source.assignments),
        courses=dict(source.courses),
    )


IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS", "false").lower() == "true"


def _dynamo_local_listening(host: str = "127.0.0.1", port: int | None = None) -> bool:
    port = int(os.environ.get("DYNAMO_HOST_PORT", "8000")) if port is None else port
    try:
        with socket.create_connection((host, port), timeout=0.4):
            return True
    except OSError:
        return False


_SKIP_DYNAMO = IN_GITHUB_ACTIONS or not _dynamo_local_listening()


@pytest.mark.skipif(
    _SKIP_DYNAMO,
    reason="GitHub Actions ou DynamoDB Local (127.0.0.1:8000) indisponível",
)
class TestDisciplinaRepositoryDynamo:
    def test_get_all_disciplinas_matches_mock_after_seed(self):
        _configure_test_env()
        dynamo = DisciplinaRepositoryDynamo()
        mock = DisciplinaRepositoryMock()
        for d in mock.disciplinas:
            dynamo.create_disciplina(d)

        resp = dynamo.get_all_disciplinas()
        mock_resp = mock.get_all_disciplinas()

        assert resp is not None
        assert isinstance(resp, list)

        codes_mock = sorted(d.code for d in mock_resp)
        codes_dynamo = sorted(d.code for d in resp if d.code in set(codes_mock))
        assert codes_dynamo == codes_mock

    def test_create_disciplina(self):
        _configure_test_env()
        dynamo = DisciplinaRepositoryDynamo()
        mock = DisciplinaRepositoryMock()
        sample = _clone_with_code(mock.disciplinas[0], _unique_code("CRT"))

        resp = dynamo.create_disciplina(sample)
        assert resp is not None
        assert resp.code == sample.code
        assert resp.name == sample.name
        assert resp.course == mock.disciplinas[0].course

    def test_create_disciplina_invalid(self):
        _configure_test_env()
        dynamo = DisciplinaRepositoryDynamo()
        with pytest.raises(Exception) as excinfo:
            dynamo.create_disciplina(None)  # type: ignore[arg-type]
        assert "attribute" in str(excinfo.value).lower()

    def test_get_disciplina(self):
        _configure_test_env()
        dynamo = DisciplinaRepositoryDynamo()
        mock = DisciplinaRepositoryMock()
        code = _unique_code("GET")
        to_save = _clone_with_code(mock.disciplinas[0], code)
        dynamo.create_disciplina(to_save)

        resp = dynamo.get_disciplina(code)
        assert resp is not None
        assert resp.model_dump(mode="json") == to_save.model_dump(mode="json")

    def test_get_disciplina_not_found(self):
        _configure_test_env()
        dynamo = DisciplinaRepositoryDynamo()
        assert dynamo.get_disciplina("non-existent-code-xyz") is None

    def test_update_disciplina(self):
        _configure_test_env()
        dynamo = DisciplinaRepositoryDynamo()
        mock = DisciplinaRepositoryMock()
        code = _unique_code("UPD")
        base = _clone_with_code(mock.disciplinas[0], code)
        dynamo.create_disciplina(base)

        updated = Disciplina(
            course=base.course,
            name="Nome atualizado pós-PUT",
            code=base.code,
            period=base.period,
            exam_weight=0.55,
            assignment_weight=0.45,
            exams=[ItemAvaliacao(name="P1", weight=0.55)],
            assignments=[ItemAvaliacao(name="T1", weight=0.45)],
            courses={"ECM": 2},
        )
        resp = dynamo.update_disciplina(updated)
        assert resp is not None
        assert resp.name == "Nome atualizado pós-PUT"
        loaded = dynamo.get_disciplina(code)
        assert loaded is not None
        assert loaded.model_dump(mode="json") == updated.model_dump(mode="json")

    def test_update_disciplina_not_found(self):
        _configure_test_env()
        dynamo = DisciplinaRepositoryDynamo()
        ghost = Disciplina(
            course="X",
            name="Y",
            code="no-such-code-999",
            period="2024.1",
            exam_weight=0.5,
            assignment_weight=0.5,
            exams=[ItemAvaliacao(name="P1", weight=0.5)],
            assignments=[ItemAvaliacao(name="T1", weight=0.5)],
            courses={"X": 1},
        )
        assert dynamo.update_disciplina(ghost) is None

    def test_delete_disciplina(self):
        _configure_test_env()
        dynamo = DisciplinaRepositoryDynamo()
        mock = DisciplinaRepositoryMock()
        code = _unique_code("DEL")
        to_save = _clone_with_code(mock.disciplinas[1], code)
        dynamo.create_disciplina(to_save)

        resp = dynamo.delete_disciplina(code)
        assert resp is not None
        assert resp.code == code
        assert dynamo.get_disciplina(code) is None

    def test_delete_disciplina_not_found(self):
        _configure_test_env()
        dynamo = DisciplinaRepositoryDynamo()
        assert dynamo.delete_disciplina("non-existent-delete-code") is None

    def test_get_all_disciplinas_escopo_global_nao_aparece_para_usuario(self):
        _configure_test_env()
        code = _unique_code("SCOPE")
        global_repo = DisciplinaRepositoryDynamo(user_id=None)
        user_repo = DisciplinaRepositoryDynamo(user_id="bob")
        mock = DisciplinaRepositoryMock()
        to_save = _clone_with_code(mock.disciplinas[0], code)
        global_repo.create_disciplina(to_save)

        user_list = user_repo.get_all_disciplinas()
        assert all(d.code != code for d in user_list)

        global_list = global_repo.get_all_disciplinas()
        assert any(d.code == code for d in global_list)
