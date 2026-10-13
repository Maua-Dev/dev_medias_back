"""Chaves single-table: PK = {owner}#{tipo}#{codigo_negocio}, SK fixa METADATA (registro canônico)."""

from enum import Enum
from typing import Any, Optional

GLOBAL_OWNER = "GLOBAL"
# SK fixa: um item por entidade; reserva o prefixo da SK para linhas filhas no futuro (ex.: NOTA#..., LOG#...).
SK_ENTITY_RECORD = "METADATA"


class EntityKind(str, Enum):
    CURSO = "CURSO"
    DISCIPLINA = "DISCIPLINA"


def normalize_owner_id(user_id: Optional[str]) -> str:
    if user_id is None or not str(user_id).strip():
        return GLOBAL_OWNER
    # '#' separa segmentos na PK; remove da id do usuário para não quebrar o formato.
    return str(user_id).strip().replace("#", "_")


def build_partition_key(owner: str, kind: EntityKind, business_code: str) -> str:
    code = str(business_code).strip()
    return f"{owner}#{kind.value}#{code}"


def strip_dynamo_metadata(item: dict[str, Any]) -> dict[str, Any]:
    out = {k: v for k, v in item.items() if k not in ("pk", "sk", "entity_type")}
    return out
