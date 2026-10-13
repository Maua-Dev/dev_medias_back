"""
Carrega os cursos do mock no DynamoDB local (escopo GLOBAL).

Execute na raiz do repositório:

    STAGE=TEST python iac/local/docker/dynamo/load_curso_mock_to_dynamo.py
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[4]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.shared.infra.external.dynamo.academic_catalog_table_setup import (
    ensure_academic_catalog_table,
)
from src.shared.infra.repositories.curso_repository_dynamo import CursoRepositoryDynamo
from src.shared.infra.repositories.curso_repository_mock import CursoRepositoryMock


def main() -> None:
    ensure_academic_catalog_table()
    mock = CursoRepositoryMock()
    repo = CursoRepositoryDynamo(user_id=None)
    n = 0
    for curso in mock.cursos:
        repo.create_curso(curso)
        n += 1
    print(f"Inseridos {n} cursos no Dynamo (GLOBAL).")


if __name__ == "__main__":
    main()
