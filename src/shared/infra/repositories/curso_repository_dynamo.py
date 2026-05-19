import json
from decimal import Decimal
from typing import List, Optional

from boto3.dynamodb.conditions import Attr

from src.shared.domain.entities.curso import Curso
from src.shared.domain.repositories.curso_repository_interface import ICursoRepository
from src.shared.environments import Environments
from src.shared.infra.external.dynamo.dynamo_datasource import DynamoDatasource
from src.shared.infra.external.dynamo.dynamo_scan_utils import scan_all_pages
from src.shared.infra.external.dynamo.academic_catalog.single_table_keys import (
    EntityKind,
    SK_ENTITY_RECORD,
    build_partition_key,
    normalize_owner_id,
    strip_dynamo_metadata,
)


def _dynamo_to_plain(obj):
    if isinstance(obj, Decimal):
        if obj == obj.to_integral_value():
            return int(obj)
        return float(obj)
    if isinstance(obj, dict):
        return {k: _dynamo_to_plain(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_dynamo_to_plain(v) for v in obj]
    return obj


class CursoRepositoryDynamo(ICursoRepository):
    """
    Single-table: pk = {owner}#CURSO#{código}, sk = METADATA.
    owner = GLOBAL (público / não logado) ou id do usuário (cursos próprios).
    """

    PARTITION_ATTR = "pk"
    SORT_ATTR = "sk"

    def __init__(self, user_id: Optional[str] = None) -> None:
        self._owner = normalize_owner_id(user_id)
        envs = Environments.get_envs()
        self.dynamo = DynamoDatasource(
            endpoint_url=envs.endpoint_url,
            dynamo_table_name=envs.academic_catalog_table_name,
            region=envs.region,
            partition_key=self.PARTITION_ATTR,
            sort_key=self.SORT_ATTR,
        )

    def _pk(self, código: str) -> str:
        return build_partition_key(self._owner, EntityKind.CURSO, código)

    def _item_to_curso(self, item: dict) -> Curso:
        return Curso.model_validate(_dynamo_to_plain(strip_dynamo_metadata(item)))

    def _curso_to_stored_item(self, curso: Curso) -> dict:
        body = json.loads(curso.model_dump_json())
        pk = self._pk(curso.código)
        return {
            **body,
            "pk": pk,
            "sk": SK_ENTITY_RECORD,
            "entity_type": EntityKind.CURSO.value,
        }

    def create_curso(self, curso: Curso) -> Optional[Curso]:
        item = self._curso_to_stored_item(curso)
        self.dynamo.put_item(
            item=item,
            partition_key=item["pk"],
            sort_key=SK_ENTITY_RECORD,
        )
        return curso

    def get_curso(self, código: str) -> Optional[Curso]:
        resp = self.dynamo.get_item(
            partition_key=self._pk(código),
            sort_key=SK_ENTITY_RECORD,
        )
        raw = resp.get("Item")
        if not raw:
            return None
        return self._item_to_curso(raw)

    def update_curso(self, curso: Curso) -> Optional[Curso]:
        existing = self.dynamo.get_item(
            partition_key=self._pk(curso.código),
            sort_key=SK_ENTITY_RECORD,
        )
        if not existing.get("Item"):
            return None
        item = self._curso_to_stored_item(curso)
        self.dynamo.put_item(
            item=item,
            partition_key=item["pk"],
            sort_key=SK_ENTITY_RECORD,
        )
        return curso

    def delete_curso(self, código: str) -> Optional[Curso]:
        existing = self.dynamo.get_item(
            partition_key=self._pk(código),
            sort_key=SK_ENTITY_RECORD,
        )
        raw = existing.get("Item")
        if not raw:
            return None
        removed = self._item_to_curso(raw)
        self.dynamo.delete_item(
            partition_key=self._pk(código),
            sort_key=SK_ENTITY_RECORD,
        )
        return removed

    def get_all_cursos(self) -> List[Curso]:
        prefix = f"{self._owner}#{EntityKind.CURSO.value}#"
        fe = Attr("entity_type").eq(EntityKind.CURSO.value) & Attr("pk").begins_with(prefix)
        items = scan_all_pages(self.dynamo.dynamo_table, FilterExpression=fe)
        return [self._item_to_curso(i) for i in items]
