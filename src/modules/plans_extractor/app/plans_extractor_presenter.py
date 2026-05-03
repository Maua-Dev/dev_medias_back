import logging
import re
import unicodedata
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

COURSE_CODE_BY_FOLDER = {
    "administracao": "ADM",
    "analise e desenvolvimento de sistemas": "ADS",
    "arquitetura e urbanismo": "ARQ",
    "ciencia da computacao": "CIC",
    "design": "DSG",
    "economia": "UNK",
    "engenharia civil": "ECV",
    "engenharia de alimentos": "EAL",
    "engenharia de computacao": "ECM",
    "engenharia de controle e automacao": "ECA",
    "engenharia de producao": "EPM",
    "engenharia eletrica": "EET",
    "engenharia eletronica": "EEN",
    "engenharia mecanica": "EMC",
    "engenharia quimica": "EQM",
    "relacoes internacionais": "RI",
    "sistemas da informacao": "SIN",
    "sistemas de informacao": "SIN",
}

COURSE_NAME_BY_FOLDER = {
    "administracao": "Administração",
    "analise e desenvolvimento de sistemas": "Análise e Desenvolvimento de Sistemas",
    "arquitetura e urbanismo": "Arquitetura e Urbanismo",
    "ciencia da computacao": "Ciência da Computação",
    "design": "Design",
    "economia": "Economia",
    "engenharia civil": "Engenharia Civil",
    "engenharia de alimentos": "Engenharia de Alimentos",
    "engenharia de computacao": "Engenharia de Computação",
    "engenharia de controle e automacao": "Engenharia de Controle e Automação",
    "engenharia de producao": "Engenharia de Produção",
    "engenharia eletrica": "Engenharia Elétrica",
    "engenharia eletronica": "Engenharia Eletrônica",
    "engenharia mecanica": "Engenharia Mecânica",
    "engenharia quimica": "Engenharia Química",
    "relacoes internacionais": "Relações Internacionais",
    "sistemas da informacao": "Sistemas da Informação",
    "sistemas de informacao": "Sistemas de Informação",
}


def _normalize_folder_name(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    without_accents = "".join(char for char in normalized if not unicodedata.combining(char))
    return " ".join(without_accents.casefold().split())


def _course_code_from_folder(folder_name: str) -> str:
    normalized = _normalize_folder_name(folder_name)
    course_code = COURSE_CODE_BY_FOLDER.get(normalized)
    if course_code is None:
        logger.warning("Could not map course folder '%s' to a known code; using UNK", folder_name)
        return "UNK"
    return course_code


def _course_name_from_folder(folder_name: str) -> str:
    normalized = _normalize_folder_name(folder_name)
    canonical = COURSE_NAME_BY_FOLDER.get(normalized)
    if canonical is not None:
        return canonical
    return " ".join(folder_name.strip().split())


def _course_code_from_legacy_token(course_token: str) -> str:
    # Legacy flat filenames may include either the course code (ADM) or the
    # course name (e.g. "Administracao"). Normalize both to the canonical code.
    token = " ".join(course_token.strip().split())
    if not token:
        return "UNK"

    upper_token = token.upper()
    if upper_token in set(COURSE_CODE_BY_FOLDER.values()):
        return upper_token

    return _course_code_from_folder(token)


def _series_number_from_folder(folder_name: str) -> int:
    match = re.search(r"\d+", folder_name)
    if not match:
        raise ValueError(f"Could not extract series number from folder: {folder_name}")
    return int(match.group())


def _s3_client():
    envs = Environments.get_envs()
    return boto3.client("s3", region_name=envs.region)


def _repository() -> DisciplinaRepositoryDynamo:
    return Environments.get_disciplina_repo()


def _parse_s3_key(key: str) -> tuple[str, str | None, int | None, str | None]:
    """Extract `(code, curso_code, ano, course_name)` from an S3 key.

    Accepts both the structured path layout (`{Curso}/{Série}/{CODE}.pdf`) and
    the legacy flat naming (`{CODE}_{CURSO}_{ANO}.pdf`). When neither layout
    matches, only the disciplina code is returned and curso/ano are left as
    `None` so the caller can persist the disciplina without polluting
    `courses` with bogus data. The folder name is also normalized to a
    canonical course display name when available.
    """
    path = PurePosixPath(unquote_plus(key))
    filename = path.name
    if not filename.lower().endswith(".pdf"):
        raise ValueError(f"S3 object is not a PDF: {key}")

    stem = filename[:-4]
    if "_" in stem:
        try:
            code, curso, ano_text = stem.rsplit("_", 2)
            ano = int(ano_text)
            if code and curso:
                return code, _course_code_from_legacy_token(curso), ano, None
        except ValueError:
            pass

    parts = path.parts
    if len(parts) >= 3:
        curso_folder = parts[-3]
        serie_folder = parts[-2]
        try:
            return (
                stem,
                _course_code_from_folder(curso_folder),
                _series_number_from_folder(serie_folder),
                _course_name_from_folder(curso_folder),
            )
        except ValueError as exc:
            logger.warning("Could not parse curso/serie from %r: %s", key, exc)

    logger.warning(
        "S3 key %r does not match {CURSO}/{SERIE}/{CODE}.pdf or {CODE}_{CURSO}_{ANO}.pdf; "
        "saving disciplina without course occurrence",
        key,
    )
    return stem, None, None, None


def _key_candidates(raw_key: str) -> list[str]:
    # The S3 event sends URL-encoded keys (spaces as `+`), but macOS-uploaded
    # files often store accents in NFD form while most clients display them in
    # NFC. We try every plausible encoding so the GetObject lookup matches the
    # actual stored bytes.
    decoded = unquote_plus(raw_key)
    seen: list[str] = []
    for value in (decoded, raw_key, unicodedata.normalize("NFC", decoded), unicodedata.normalize("NFD", decoded)):
        if value and value not in seen:
            seen.append(value)
    return seen


def _download_pdf(bucket: str, raw_key: str) -> tuple[str, bytes]:
    s3 = _s3_client()
    candidates = _key_candidates(raw_key)
    last_error: Exception | None = None
    for key in candidates:
        logger.info("Downloading PDF from s3://%s/%s", bucket, key)
        try:
            response = s3.get_object(Bucket=bucket, Key=key)
            return key, response["Body"].read()
        except s3.exceptions.NoSuchKey as exc:
            logger.warning("Object not found at s3://%s/%s, trying next candidate", bucket, key)
            last_error = exc

    raise FileNotFoundError(
        f"S3 object not found in bucket {bucket} (tried keys: {candidates})"
    ) from last_error


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
    code, curso, ano, course_name = _parse_s3_key(raw_key)

    key, pdf_bytes = _download_pdf(bucket, raw_key)
    extracted_text = extract_text_from_pdf(pdf_bytes)
    if not extracted_text.strip():
        logger.warning("Skipping s3://%s/%s because no text could be extracted", bucket, key)
        return False

    extracted_data = extract_structured_data(extracted_text)
    if course_name:
        extracted_data["course"] = course_name
    course_occurrence: dict[str, int] = {curso: ano} if curso and ano is not None else {}
    disciplina = build_disciplina(extracted_data, courses=course_occurrence)

    existing = repository.get_disciplina(code)
    if existing is None:
        logger.info("Creating disciplina %s with courses=%s", code, course_occurrence)
        repository.create_disciplina(disciplina)
    elif curso and ano is not None:
        logger.info("Updating course occurrence for existing disciplina %s: %s=%s", code, curso, ano)
        _update_disciplina_courses(repository, code, curso, ano)
    else:
        logger.info(
            "Disciplina %s already exists and S3 key has no curso/serie; leaving courses untouched",
            code,
        )

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
