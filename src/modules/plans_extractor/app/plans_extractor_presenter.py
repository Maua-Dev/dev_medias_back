import logging
from pathlib import PurePosixPath
from typing import Any
from urllib.parse import unquote_plus

import boto3

from src.shared.infra.external.dynamo.single_table_keys import SK_ENTITY_RECORD
from src.shared.infra.repositories.disciplina_repository_dynamo import DisciplinaRepositoryDynamo
from src.shared.environments import Environments

from .bedrock_client import extract_structured_data
from .extractor import extract_text_from_pdf
from .parser import build_disciplina

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _s3_client():
    envs = Environments.get_envs()
    return boto3.client("s3", region_name=envs.region)


def _repository() -> DisciplinaRepositoryDynamo:
    return Environments.get_disciplina_repo()


def _parse_s3_key(key: str) -> tuple[str, str, int]:
    filename = PurePosixPath(unquote_plus(key)).name
    if not filename.lower().endswith(".pdf"):
        raise ValueError(f"S3 object is not a PDF: {key}")

    stem = filename[:-4]
    try:
        code, curso, ano_text = stem.rsplit("_", 2)
    except ValueError as exc:
        raise ValueError("S3 key must follow {CODE}_{CURSO}_{ANO}.pdf") from exc

    if not code or not curso:
        raise ValueError("S3 key must include non-empty CODE and CURSO")

    try:
        ano = int(ano_text)
    except ValueError as exc:
        raise ValueError(f"ANO must be an integer in S3 key: {key}") from exc

    return code, curso, ano


def _download_pdf(bucket: str, key: str) -> bytes:
    logger.info("Downloading PDF from s3://%s/%s", bucket, key)
    response = _s3_client().get_object(Bucket=bucket, Key=key)
    return response["Body"].read()


def _update_disciplina_courses(repository: DisciplinaRepositoryDynamo, code: str, curso: str, ano: int) -> None:
    repository.dynamo.dynamo_table.update_item(
        Key={
            repository.PARTITION_ATTR: repository._pk(code),
            repository.SORT_ATTR: SK_ENTITY_RECORD,
        },
        UpdateExpression="SET #courses.#curso = :ano",
        ExpressionAttributeNames={
            "#courses": "courses",
            "#curso": curso,
        },
        ExpressionAttributeValues={
            ":ano": ano,
        },
    )


def _process_record(record: dict[str, Any], repository: DisciplinaRepositoryDynamo) -> bool:
    bucket = record["s3"]["bucket"]["name"]
    raw_key = record["s3"]["object"]["key"]
    code, curso, ano = _parse_s3_key(raw_key)
    key = unquote_plus(raw_key)

    pdf_bytes = _download_pdf(bucket, key)
    extracted_text = extract_text_from_pdf(pdf_bytes)
    if not extracted_text.strip():
        logger.warning("Skipping s3://%s/%s because no text could be extracted", bucket, key)
        return False

    extracted_data = extract_structured_data(extracted_text)
    disciplina = build_disciplina(extracted_data, courses={curso: ano})

    existing = repository.get_disciplina(code)
    if existing is None:
        logger.info("Creating disciplina %s with course occurrence %s=%s", code, curso, ano)
        repository.create_disciplina(disciplina)
    else:
        logger.info("Updating course occurrence for existing disciplina %s: %s=%s", code, curso, ano)
        _update_disciplina_courses(repository, code, curso, ano)

    return True


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    records = event.get("Records", [])
    repository = _repository()

    processed = 0
    skipped = 0
    for record in records:
        if _process_record(record, repository):
            processed += 1
        else:
            skipped += 1

    return {"processed": processed, "skipped": skipped}
