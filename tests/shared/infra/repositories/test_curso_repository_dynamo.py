import os
import socket
import uuid

import pytest

pytest.importorskip("boto3")

from src.shared.domain.entities.curso import Curso
from src.shared.infra.repositories.curso_repository_dynamo import CursoRepositoryDynamo
from src.shared.infra.repositories.curso_repository_mock import CursoRepositoryMock


def _configure_test_env() -> None:
    os.environ["STAGE"] = "TEST"
    port = os.environ.get("DYNAMO_HOST_PORT", "8000")
    os.environ.setdefault("ENDPOINT_URL", f"http://127.0.0.1:{port}")
    os.environ.setdefault("ACADEMIC_CATALOG_TABLE_NAME", "DevMediasAcademicCatalogTable-test")


def _unique_codigo(prefix: str = "DYN") -> str:
    return f"{prefix}-{uuid.uuid4().hex[:12].upper()}"


def _clone_with_codigo(source: Curso, código: str) -> Curso:
    return Curso(código=código, nome=source.nome)


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
class TestCursoRepositoryDynamo:
    def test_get_all_cursos_matches_mock_after_seed(self):
        _configure_test_env()
        dynamo = CursoRepositoryDynamo()
        mock = CursoRepositoryMock()
        for c in mock.cursos:
            dynamo.create_curso(c)

        resp = dynamo.get_all_cursos()
        mock_resp = mock.get_all_cursos()

        assert resp is not None
        assert isinstance(resp, list)

        codes_mock = sorted(c.código for c in mock_resp)
        codes_dynamo = sorted(c.código for c in resp if c.código in set(codes_mock))
        assert codes_dynamo == codes_mock

    def test_create_curso(self):
        _configure_test_env()
        dynamo = CursoRepositoryDynamo()
        mock = CursoRepositoryMock()
        sample = _clone_with_codigo(mock.cursos[0], _unique_codigo("CRT"))

        resp = dynamo.create_curso(sample)
        assert resp is not None
        assert resp.código == sample.código
        assert resp.nome == sample.nome
        assert resp.nome == mock.cursos[0].nome

    def test_create_curso_invalid(self):
        _configure_test_env()
        dynamo = CursoRepositoryDynamo()
        with pytest.raises(Exception) as excinfo:
            dynamo.create_curso(None)  # type: ignore[arg-type]
        assert "attribute" in str(excinfo.value).lower()

    def test_get_curso(self):
        _configure_test_env()
        dynamo = CursoRepositoryDynamo()
        mock = CursoRepositoryMock()
        código = _unique_codigo("GET")
        to_save = _clone_with_codigo(mock.cursos[0], código)
        dynamo.create_curso(to_save)

        resp = dynamo.get_curso(código)
        assert resp is not None
        assert resp.model_dump(mode="json") == to_save.model_dump(mode="json")

    def test_get_curso_not_found(self):
        _configure_test_env()
        dynamo = CursoRepositoryDynamo()
        assert dynamo.get_curso("non-existent-code-xyz") is None

    def test_update_curso(self):
        _configure_test_env()
        dynamo = CursoRepositoryDynamo()
        mock = CursoRepositoryMock()
        código = _unique_codigo("UPD")
        base = _clone_with_codigo(mock.cursos[0], código)
        dynamo.create_curso(base)

        updated = Curso(código=base.código, nome="Nome atualizado pós-PUT")
        resp = dynamo.update_curso(updated)
        assert resp is not None
        assert resp.nome == "Nome atualizado pós-PUT"
        loaded = dynamo.get_curso(código)
        assert loaded is not None
        assert loaded.model_dump(mode="json") == updated.model_dump(mode="json")

    def test_update_curso_not_found(self):
        _configure_test_env()
        dynamo = CursoRepositoryDynamo()
        ghost = Curso(código="no-such-code-999", nome="Y")
        assert dynamo.update_curso(ghost) is None

    def test_delete_curso(self):
        _configure_test_env()
        dynamo = CursoRepositoryDynamo()
        mock = CursoRepositoryMock()
        código = _unique_codigo("DEL")
        to_save = _clone_with_codigo(mock.cursos[1], código)
        dynamo.create_curso(to_save)

        resp = dynamo.delete_curso(código)
        assert resp is not None
        assert resp.código == código
        assert dynamo.get_curso(código) is None

    def test_delete_curso_not_found(self):
        _configure_test_env()
        dynamo = CursoRepositoryDynamo()
        assert dynamo.delete_curso("non-existent-delete-code") is None

    def test_get_all_cursos_escopo_global_nao_aparece_para_usuario(self):
        _configure_test_env()
        código = _unique_codigo("SCOPE")
        global_repo = CursoRepositoryDynamo(user_id=None)
        user_repo = CursoRepositoryDynamo(user_id="alice")
        global_repo.create_curso(Curso(código=código, nome="Só GLOBAL"))

        user_cursos = user_repo.get_all_cursos()
        assert all(c.código != código for c in user_cursos)

        global_cursos = global_repo.get_all_cursos()
        assert any(c.código == código for c in global_cursos)
