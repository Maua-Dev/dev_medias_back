"""Scan Academic Catalog Dynamo → legacy JSON → S3."""

from __future__ import annotations

import json
import logging
import os
from decimal import Decimal
from typing import Any

import boto3
from boto3.dynamodb.conditions import Attr

from src.shared.environments import Environments
from src.shared.helpers.legacy_catalog.convert_to_legacy_json import build_legacy_catalog
from src.shared.infra.external.dynamo.dynamo_scan_utils import scan_all_pages

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

DEFAULT_SUBJECTS_KEY = "allSubjects.json"
DEFAULT_COURSES_KEY = "courses.json"


def _dynamo_to_plain(obj: Any) -> Any:
    if isinstance(obj, Decimal):
        if obj == obj.to_integral_value():
            return int(obj)
        return float(obj)
    if isinstance(obj, dict):
        return {k: _dynamo_to_plain(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_dynamo_to_plain(v) for v in obj]
    return obj


class ExportLegacyCatalogUsecase:
    def __init__(
        self,
        *,
        table_name: str | None = None,
        bucket_name: str | None = None,
        subjects_key: str | None = None,
        courses_key: str | None = None,
        region: str | None = None,
        endpoint_url: str | None = None,
        dynamodb_table: Any | None = None,
        s3_client: Any | None = None,
    ) -> None:
        envs = Environments.get_envs()
        self.table_name = table_name or envs.academic_catalog_table_name
        self.bucket_name = bucket_name or os.environ.get("LEGACY_EXPORT_BUCKET_NAME")
        self.subjects_key = subjects_key or os.environ.get(
            "LEGACY_EXPORT_SUBJECTS_KEY", DEFAULT_SUBJECTS_KEY
        )
        self.courses_key = courses_key or os.environ.get(
            "LEGACY_EXPORT_COURSES_KEY", DEFAULT_COURSES_KEY
        )
        self.cloudfront_distribution_id = (
            os.environ.get("LEGACY_EXPORT_CLOUDFRONT_DISTRIBUTION_ID") or ""
        ).strip()
        self.region = region or envs.region or os.environ.get("AWS_REGION") or "us-east-1"
        self.endpoint_url = endpoint_url if endpoint_url is not None else envs.endpoint_url

        if dynamodb_table is not None:
            self._table = dynamodb_table
        else:
            resource = boto3.resource(
                "dynamodb",
                region_name=self.region,
                endpoint_url=self.endpoint_url,
            )
            self._table = resource.Table(self.table_name)

        self._s3 = s3_client or boto3.client("s3", region_name=self.region)
        self._cloudfront = boto3.client("cloudfront", region_name="us-east-1")

    def _scan_catalog_items(self) -> list[dict[str, Any]]:
        fe = Attr("entity_type").is_in(["DISCIPLINA", "CURSO"])
        raw_items = scan_all_pages(self._table, FilterExpression=fe)
        return [_dynamo_to_plain(item) for item in raw_items]

    def _put_json(self, key: str, payload: dict[str, Any]) -> str:
        body = json.dumps(payload, ensure_ascii=False, indent=4) + "\n"
        self._s3.put_object(
            Bucket=self.bucket_name,
            Key=key,
            Body=body.encode("utf-8"),
            ContentType="application/json; charset=utf-8",
        )
        return f"s3://{self.bucket_name}/{key}"

    def __call__(self) -> dict[str, Any]:
        if not self.bucket_name:
            raise ValueError("LEGACY_EXPORT_BUCKET_NAME is required")

        items = self._scan_catalog_items()
        all_subjects, courses, report_meta = build_legacy_catalog(items)

        subjects_uri = self._put_json(self.subjects_key, all_subjects)
        courses_uri = self._put_json(self.courses_key, courses)

        invalidation_id = None
        if self.cloudfront_distribution_id:
            invalidation_id = self._invalidate_cdn(
                [f"/{self.subjects_key}", f"/{self.courses_key}"]
            )

        result = {
            "ok": True,
            "table": self.table_name,
            "subjects_uri": subjects_uri,
            "courses_uri": courses_uri,
            "cloudfront_invalidation_id": invalidation_id,
            **report_meta,
        }
        logger.info(
            "Exported legacy catalog: subjects=%s courses=%s skipped=%s invalidation=%s",
            result["subjects_count"],
            result["courses_count"],
            result["skipped_non_global_or_custom"],
            invalidation_id,
        )
        return result

    def _invalidate_cdn(self, paths: list[str]) -> str:
        resp = self._cloudfront.create_invalidation(
            DistributionId=self.cloudfront_distribution_id,
            InvalidationBatch={
                "Paths": {"Quantity": len(paths), "Items": paths},
                "CallerReference": f"export-legacy-catalog-{os.urandom(8).hex()}",
            },
        )
        return resp["Invalidation"]["Id"]
