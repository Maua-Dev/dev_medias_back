import json
import logging
import re
import unicodedata
from pathlib import PurePosixPath
from typing import Any
from urllib.parse import unquote_plus

import pymupdf
from botocore.exceptions import ClientError

from .helper.course.course import Course
from .parser import build_disciplina
from src.shared.environments import Environments
from src.shared.infra.repositories.disciplina_repository_dynamo import DisciplinaRepositoryDynamo

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

HEADER_CROP_COORDS = pymupdf.Rect(0, 0, 595, 620)

INFO_COORDS: dict[str, pymupdf.Rect] = {
    "course_code": pymupdf.Rect(396, 715, 564, 730),
    "course_name": pymupdf.Rect(25, 717, 396, 729)
}

COURSE_CRITERIA_HEADER_REGEX = re.compile(r"AVALIAÇÃO (.*) e CRITÉRIOS DE APROVAÇÃO", re.IGNORECASE)
COURSE_EXAMS_AND_PROJECTS_HEADER_REGEX = re.compile(
    r"INFORMA[ÇC][ÕO]ES?\s+SOBRE\s+PROVAS?\s+E\s+TRABALHOS?",
    re.IGNORECASE,
)
COURSE_PROGRAM_HEADER_REGEX = re.compile(r"PROGRAMA DA DISCIPLINA", re.IGNORECASE)

END_EXTRACTION_REGEX = re.compile(r"PLANO DE ENSINO PARA O ANO LETIVO DE \d{4}", re.IGNORECASE)
EVALUATION_SIGNAL_REGEXES = (
    re.compile(r"PESO\s+DE\s+MP\s*\(?(?:kp|k p)\)?", re.IGNORECASE),
    re.compile(r"PESO\s+DE\s+MT\s*\(?(?:kt|k t)\)?", re.IGNORECASE),
    re.compile(r"\b(?:T\d+[A-Z]?|P\d+|PSUB)\b", re.IGNORECASE),
    re.compile(r"CRIT[ÉE]RIO\s+DE\s+AVALIA", re.IGNORECASE),
    re.compile(r"INFORMA[ÇC][ÕO]ES?\s+SOBRE\s+PROVAS?\s+E\s+TRABALHOS?", re.IGNORECASE),
    re.compile(r"PROVA\s+SUB(?:STITUTIVA|STITUTA)?", re.IGNORECASE),
    re.compile(r"M[ÉE]DIA\s+DE\s+(?:PROVAS|TRABALHOS)", re.IGNORECASE),
)
EVALUATION_RELEVANT_LINE_REGEX = re.compile(
    r"(PESO|PROVA|TRABALH|CRIT[ÉE]RIO\s+DE\s+AVALIA|(?:\bT\d+[A-Z]?\b)|(?:\bP\d+\b)|PSUB|MP|MT|k\d+)",
    re.IGNORECASE,
)


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


def _series_number_from_folder(folder_name: str) -> int:
    match = re.search(r"\d+", folder_name)
    if not match:
        raise ValueError(f"Could not extract series number from folder: {folder_name}")
    return int(match.group())


def _parse_s3_key(key: str) -> tuple[str, str | None, int | None, str | None]:
    """Extract `(code, curso_code, ano, course_name)` from an S3 key.
    
    Expects path format: {Curso}/{Série}/{CODE}.pdf
    Example: Ciência da Computação/1o semestre/Banco de dados.pdf
    """
    path = PurePosixPath(unquote_plus(key))
    filename = path.name
    if not filename.lower().endswith(".pdf"):
        raise ValueError(f"S3 object is not a PDF: {key}")

    stem = filename[:-4]
    
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
        "S3 key %r does not match {CURSO}/{SERIE}/{CODE}.pdf format; "
        "saving disciplina without course occurrence",
        key,
    )
    return stem, None, None, None

def extract_course_info_from_header(page: pymupdf.Page) -> dict[str, str]:
    ptm = page.transformation_matrix
    info_dict = {}

    for key, rect in INFO_COORDS.items():
        info = page.get_textbox(rect * ~ptm)
        if info == "":
            raise ValueError(f"Could not extract {key} from the PDF.")
        info_dict[key] = info

    return info_dict

def extract_course_criteria(doc: pymupdf.Document) -> str:
    extracting = False
    criteria_text = ""

    for page in doc:
        ptm = page.transformation_matrix
        page.set_cropbox(HEADER_CROP_COORDS * ~ptm)

        text = page.get_text()
        for line in text.splitlines():
            if COURSE_CRITERIA_HEADER_REGEX.search(line):
                extracting = True
                continue
            elif END_EXTRACTION_REGEX.search(line):
                extracting = False

            if extracting:
                criteria_text += line + "\n"

    if criteria_text == "":
        raise ValueError("Could not extract course criteria from the PDF.")
    
    return criteria_text

def extract_course_exams_and_projects_info(doc: pymupdf.Document) -> str:
    extracting = False
    exams_and_projects_text = ""

    for page in doc:
        text = page.get_text()
        for line in text.splitlines():
            if COURSE_EXAMS_AND_PROJECTS_HEADER_REGEX.search(line):
                extracting = True
                continue
            elif END_EXTRACTION_REGEX.search(line):
                extracting = False

            if extracting:
                exams_and_projects_text += line + "\n"

    if exams_and_projects_text.strip() and _has_evaluation_signal(exams_and_projects_text):
        return exams_and_projects_text

    if exams_and_projects_text.strip():
        logger.warning("Primary exams/projects extraction looked uninformative; trying fallback")

    if exams_and_projects_text == "" or not _has_evaluation_signal(exams_and_projects_text):
        fallback_text = _extract_exams_and_projects_fallback_text(doc)
        if fallback_text:
            logger.warning("Using fallback extraction for exams and projects section")
            return fallback_text
        raise ValueError("Could not extract exams and projects info from the PDF.")
    
    return exams_and_projects_text


def _has_evaluation_signal(text: str) -> bool:
    return any(regex.search(text) for regex in EVALUATION_SIGNAL_REGEXES)


def _extract_exams_and_projects_fallback_text(doc: pymupdf.Document) -> str:
    lines: list[str] = []
    for page in doc:
        lines.extend(page.get_text().splitlines())

    useful_lines: list[str] = []
    seen: set[str] = set()
    for index, line in enumerate(lines):
        if not any(regex.search(line) for regex in EVALUATION_SIGNAL_REGEXES):
            continue

        start = max(0, index - 1)
        end = min(len(lines), index + 2)
        for candidate in lines[start:end]:
            normalized = candidate.strip()
            if not normalized:
                continue
            if not EVALUATION_RELEVANT_LINE_REGEX.search(normalized):
                continue
            if normalized in seen:
                continue
            seen.add(normalized)
            useful_lines.append(normalized)

    return "\n".join(useful_lines)


def extract_course_program(doc: pymupdf.Document) -> str:
    extracting = False
    program_text = ""

    for page in doc:
        text = page.get_text()
        for line in text.splitlines():
            if COURSE_PROGRAM_HEADER_REGEX.search(line):
                extracting = True
                continue

            if extracting:
                program_text += line + "\n"

    return program_text

def generate_json_with_bedrock(course_info: Course, bedrock_client: Any | None = None) -> dict[str, Any]:
    PROMPT_TEMPLATE = """Você é um extrator de dados acadêmicos. A partir do dicionário Python abaixo (gerado por um script de scraping), extraia e estruture as informações no formato JSON especificado.

    ## Entrada
    ```
    {INPUT_DATA}
    ```

    ## Saída esperada
    Retorne APENAS um JSON válido, sem texto adicional, sem markdown, sem explicações. O JSON deve seguir exatamente esta estrutura:

    {{
      "course": "<nome completo da disciplina>",
      "name": "<nome completo da disciplina, mesmo que 'course'>",
      "code": "<código da disciplina, ex: EFB1002>",
      "period": "<período da disciplina se disponível, senão null>",
      "examWeight": <peso das provas como número entre 0 e 1, ex: 0.5>,
      "assignmentWeight": <peso dos trabalhos como número entre 0 e 1, ex: 0.5>,
      "exams": [
        {{
          "name": "<nome descritivo, ex: Primeira Prova Bimestral>",
          "weight": <peso relativo desta prova dentro das provas, entre 0 e 1>
        }}
      ],
      "assignments": [
        {{
          "name": "<nome descritivo, ex: Trabalho do Primeiro Bimestre>",
          "weight": <peso relativo deste trabalho dentro dos trabalhos, entre 0 e 1>
        }}
      ],
      "courses": {{}}
    }}

    ## Regras de extração
    - "course" deve ser o nome da disciplina presente no PDF; o backend sobrescreve esse campo com o nome do curso vindo da pasta do S3 antes de persistir.
    - "examWeight" vem do campo "Peso de MP(kp)" dividido pela soma de kp+kt (ex: kp=5, kt=5 → examWeight=0.5)
    - "assignmentWeight" vem do campo "Peso de MT(kt)" dividido pela soma de kp+kt
    - Ao extrair "exams" e "assignments", use prioritariamente o trecho "INFORMAÇÕES SOBRE PROVAS E TRABALHOS" quando ele existir.
    - Se houver pontuação explícita para componentes avaliativos (ex.: "X vale 2", "Y vale 6"), calcule os pesos relativos dividindo cada valor pela soma total dos valores do grupo.
    - Só use distribuição de pesos iguais quando não houver qualquer informação explícita de pontuação ou peso no texto.
    - Para disciplina anual com duas provas semestrais, aplicar pesos 2/5 e 3/5 (RN CEPE 16/2014), preferindo primeiro semestre=0.4 e segundo semestre=0.6 quando identificados
    - Para disciplina semestral, distribuir pesos das provas por média simples quando não houver pesos explícitos
    - "exams" deve listar todas as provas mencionadas (P1, P2, PS1, etc.), inclusive quando elas aparecem no programa da disciplina.
    - Para provas bimestrais com pesos iguais, cada uma recebe weight = 1 / (número de provas regulares)
    - "assignments" deve listar todos os trabalhos mencionados (T1, T2, T3, projeto, relatório, etc.) com pesos coerentes com os valores explícitos; na ausência deles, usar pesos iguais.
    - "period" deve ser extraído se mencionado (ex: "1º semestre de 2024"), senão null
    - "courses" deve ser sempre um objeto vazio {{}}
    - Todos os campos numéricos de peso devem ser números (não strings)"""

    if bedrock_client is None:
        import boto3

        client = boto3.client("bedrock-runtime", region_name="us-east-1")
    else:
        client = bedrock_client
    model_id = "amazon.nova-lite-v1:0"

    PROMPT = PROMPT_TEMPLATE.format(INPUT_DATA=json.dumps(course_info.__dict__, ensure_ascii=False))

    native_request = {
        "messages": [
            {
                "role": "user",
                "content": [{"text": PROMPT}],
            }
        ],
        "inferenceConfig": {
            "max_new_tokens": 1000,
            "temperature": 0,
        },
    }

    request = json.dumps(native_request)

    try:
        response = client.invoke_model(modelId=model_id, body=request)
    except (ClientError, Exception) as e:
        logger.error("ERROR: Can't invoke '%s'. Reason: %s", model_id, e)
        raise

    model_response = json.loads(response["body"].read())
    response_text = model_response["output"]["message"]["content"][0]["text"]
    
    if response_text.startswith("```"):
        response_text = response_text.split("```")[1]
        if response_text.startswith("json"):
            response_text = response_text[4:]
        response_text = response_text.strip()

    logger.info("Bedrock response: %s", response_text)
    return json.loads(response_text)

def _key_candidates(raw_key: str) -> list[str]:
    decoded = unquote_plus(raw_key)
    seen: list[str] = []
    for value in (decoded, raw_key, unicodedata.normalize("NFC", decoded), unicodedata.normalize("NFD", decoded)):
        if value and value not in seen:
            seen.append(value)
    return seen


def load_pdf_from_s3(bucket: str, key: str) -> pymupdf.Document:
    """Download PDF from S3 and return as pymupdf Document."""
    import boto3

    s3 = boto3.client("s3")

    last_error: Exception | None = None
    for candidate_key in _key_candidates(key):
        logger.info("Loading s3://%s/%s", bucket, candidate_key)
        try:
            response = s3.get_object(Bucket=bucket, Key=candidate_key)
            pdf_bytes = response["Body"].read()
            return pymupdf.open(stream=pdf_bytes, filetype="pdf")
        except s3.exceptions.NoSuchKey as exc:
            logger.warning("Object not found at s3://%s/%s, trying next candidate", bucket, candidate_key)
            last_error = exc
        except Exception as exc:
            logger.error("Error getting object %s from bucket %s: %s", candidate_key, bucket, exc)
            raise

    raise FileNotFoundError(f"S3 object not found in bucket {bucket} (tried keys: {_key_candidates(key)})") from last_error


def _repository() -> DisciplinaRepositoryDynamo:
    """Get DynamoDB repository instance."""
    return Environments.get_disciplina_repo()


def _process_s3_record(record: dict[str, Any], repository: DisciplinaRepositoryDynamo) -> bool:
    """Process a single S3 event record and persist extracted disciplina to DynamoDB."""
    try:
        bucket = record["s3"]["bucket"]["name"]
        raw_key = record["s3"]["object"]["key"]
        
        code, curso, ano, course_name = _parse_s3_key(raw_key)
        logger.info("Parsed S3 key: code=%s, curso=%s, ano=%s, course_name=%s", code, curso, ano, course_name)
        
        doc = load_pdf_from_s3(bucket, raw_key)

        header_info = extract_course_info_from_header(doc[0])

        course_criteria = extract_course_criteria(doc)

        exams_and_projects_info = extract_course_exams_and_projects_info(doc)
        course_program = extract_course_program(doc)

        course = Course(
            name=header_info["course_name"],
            code=header_info["course_code"],
            criteria=course_criteria,
            exams_and_projects_info=f"{exams_and_projects_info}\nPROGRAMA DA DISCIPLINA\n{course_program}",
        )

        extracted_data = generate_json_with_bedrock(course)
        # Source of truth for disciplina code is the S3 object key.
        # This avoids model hallucinations/variations (e.g., EEN281 -> EEE281)
        # that would persist under the wrong primary key in Dynamo.
        extracted_data["code"] = code
        
        if course_name:
            extracted_data["course"] = course_name
        
        existing = repository.get_disciplina(code)
        course_occurrence: dict[str, int] = {curso: ano} if curso and ano is not None else {}
        if existing is None:
            courses_to_persist = course_occurrence
        else:
            courses_to_persist = dict(existing.courses)
            courses_to_persist.update(course_occurrence)

        disciplina = build_disciplina(extracted_data, courses=courses_to_persist)

        if existing is None:
            logger.info("Creating disciplina %s with courses=%s", code, courses_to_persist)
            repository.create_disciplina(disciplina)
        else:
            logger.info("Updating existing disciplina %s", code)
            repository.update_disciplina(disciplina)

        return True
    except Exception as e:
        logger.error("Error processing S3 record: %s", e)
        return False


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """AWS Lambda handler for processing syllabus PDFs from S3."""
    records = event.get("Records", [])
    repository = _repository()

    processed = 0
    skipped = 0
    for record in records:
        if _process_s3_record(record, repository):
            processed += 1
        else:
            skipped += 1

    logger.info("Lambda execution complete: processed=%d, skipped=%d", processed, skipped)
    return {"processed": processed, "skipped": skipped}
