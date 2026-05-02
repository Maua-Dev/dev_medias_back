import json
from decimal import Decimal
from typing import List, Optional

from boto3.dynamodb.conditions import Attr

from src.shared.domain.entities.disciplina import Disciplina
from src.shared.domain.repositories.disciplina_repository_interface import IDisciplinaRepository
from src.shared.environments import Environments
from src.shared.infra.external.dynamo.dynamo_datasource import DynamoDatasource
from src.shared.infra.external.dynamo.dynamo_scan_utils import scan_all_pages
from src.shared.infra.external.dynamo.single_table_keys import (
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


class DisciplinaRepositoryDynamo(IDisciplinaRepository):
    """
    Single-table: pk = {owner}#DISCIPLINA#{code}, sk = METADATA.
    owner = GLOBAL (catálogo padrão) ou id do usuário (disciplinas próprias).
    """

    PARTITION_ATTR = "pk"
    SORT_ATTR = "sk"

    def __init__(self, user_id: Optional[str] = None) -> None:
        self._owner = normalize_owner_id(user_id)
        envs = Environments.get_envs()
        self.dynamo = DynamoDatasource(
            endpoint_url=envs.endpoint_url,
            dynamo_table_name=envs.entity_table_name,
            region=envs.region,
            partition_key=self.PARTITION_ATTR,
            sort_key=self.SORT_ATTR,
        )

    def _pk(self, code: str) -> str:
        return build_partition_key(self._owner, EntityKind.DISCIPLINA, code)

    def _item_to_disciplina(self, item: dict) -> Disciplina:
        return Disciplina.model_validate(_dynamo_to_plain(strip_dynamo_metadata(item)))

    def _disciplina_to_stored_item(self, disciplina: Disciplina) -> dict:
        body = json.loads(disciplina.model_dump_json())
        pk = self._pk(disciplina.code)
        return {
            **body,
            "pk": pk,
            "sk": SK_ENTITY_RECORD,
            "entity_type": EntityKind.DISCIPLINA.value,
        }

    def create_disciplina(self, disciplina: Disciplina) -> Optional[Disciplina]:
        item = self._disciplina_to_stored_item(disciplina)
        self.dynamo.put_item(
            item=item,
            partition_key=item["pk"],
            sort_key=SK_ENTITY_RECORD,
        )
        return disciplina

    def get_disciplina(self, code: str) -> Optional[Disciplina]:
        resp = self.dynamo.get_item(
            partition_key=self._pk(code),
            sort_key=SK_ENTITY_RECORD,
        )
        raw = resp.get("Item")
        if not raw:
            return None
        return self._item_to_disciplina(raw)

    def update_disciplina(self, disciplina: Disciplina) -> Optional[Disciplina]:
        existing = self.dynamo.get_item(
            partition_key=self._pk(disciplina.code),
            sort_key=SK_ENTITY_RECORD,
        )
        if not existing.get("Item"):
            return None
        item = self._disciplina_to_stored_item(disciplina)
        self.dynamo.put_item(
            item=item,
            partition_key=item["pk"],
            sort_key=SK_ENTITY_RECORD,
        )
        return disciplina

    def delete_disciplina(self, code: str) -> Optional[Disciplina]:
        existing = self.dynamo.get_item(
            partition_key=self._pk(code),
            sort_key=SK_ENTITY_RECORD,
        )
        raw = existing.get("Item")
        if not raw:
            return None
        removed = self._item_to_disciplina(raw)
        self.dynamo.delete_item(
            partition_key=self._pk(code),
            sort_key=SK_ENTITY_RECORD,
        )
        return removed

    def get_all_disciplinas(self) -> List[Disciplina]:
        prefix = f"{self._owner}#{EntityKind.DISCIPLINA.value}#"
        fe = Attr("entity_type").eq(EntityKind.DISCIPLINA.value) & Attr("pk").begins_with(prefix)
        items = scan_all_pages(self.dynamo.dynamo_table, FilterExpression=fe)
        return [self._item_to_disciplina(i) for i in items]
