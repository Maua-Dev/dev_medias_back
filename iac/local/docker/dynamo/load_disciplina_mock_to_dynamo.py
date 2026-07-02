"""
Carrega as disciplinas do mock no DynamoDB local (escopo GLOBAL).

Execute na raiz do repositório:

    STAGE=TEST python iac/local/docker/dynamo/load_disciplina_mock_to_dynamo.py
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
from src.shared.infra.repositories.disciplina_repository_dynamo import DisciplinaRepositoryDynamo
from src.shared.infra.repositories.disciplina_repository_mock import DisciplinaRepositoryMock


def main() -> None:
    ensure_academic_catalog_table()
    mock = DisciplinaRepositoryMock()
    repo = DisciplinaRepositoryDynamo(user_id=None)
    n = 0
    for disciplina in mock.disciplinas:
        repo.create_disciplina(disciplina)
        n += 1
    print(f"Inseridas {n} disciplinas no Dynamo (GLOBAL).")


if __name__ == "__main__":
    main()
