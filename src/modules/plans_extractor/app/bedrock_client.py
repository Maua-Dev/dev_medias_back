import json
import logging
import os
import re
from typing import Any

import boto3

logger = logging.getLogger(__name__)

DEFAULT_MODEL_ID = "us.anthropic.claude-haiku-4-5-20251001-v1:0"

EXTRACTION_PROMPT = """Você receberá o texto extraído de um Plano de Ensino do Instituto Mauá de Tecnologia.
Sua tarefa é extrair informações estruturadas e retornar EXCLUSIVAMENTE um objeto JSON
válido, sem texto adicional, sem markdown, sem explicações, sem blocos de código.

Schema esperado:
{
  "code": "string",
  "name": "string",
  "course": "string",
  "period": "string",
  "exam_weight": float,
  "assignment_weight": float,
  "exams": [{ "name": "string", "weight": float }],
  "assignments": [{ "name": "string", "weight": float }]
}

Regras:
- code: valor do campo "Código da Disciplina" (ex: "TNG1005")
- name: valor do campo "Disciplina" em português, em formato de título.
  Exemplo: "ENGENHARIA DE SOFTWARE" -> "Engenharia de Software"
- course: valor do campo "Materia" em português. Se vazio, use "Disciplina".
  Nunca use o campo "Course" (inglês) nem "TEMÁRIO" (espanhol)
- period: retorne SOMENTE um destes valores:
  - "S" para semestral
  - "A" para anual
  - "T" para trimestral
  Se não encontrar, retorne "A"
- exam_weight: campo "Peso de MP (kp)" como percentual de 0 a 100.
  Exemplo: 70.0 (NÃO retorne 7.0)
- assignment_weight: campo "Peso de MT (kt)" como percentual de 0 a 100.
  Exemplo: 30.0 (NÃO retorne 3.0)
- exams: lista de provas (P1, P2, PS...) com peso relativo entre 0 e 1
  (ex.: 0.5, 0.25). Se exam_weight for 0, retorne []
- Se o texto NÃO informar explicitamente a distribuição dos pesos das provas,
  use esta regra padrão por período:
  - Se period = "S": distribuição uniforme entre as provas (média simples)
    Ex.: 1 prova -> [1.0], 2 provas -> [0.5, 0.5]
  - Se period = "A" ou "T": 40% para as primeiras provas e 60% para as últimas,
    distribuindo igualmente dentro de cada grupo
  Exemplos:
  - 2 provas: [0.4, 0.6]
  - 3 provas: [0.2, 0.2, 0.6]
  - 4 provas: [0.2, 0.2, 0.3, 0.3]
- Dê preferência aos pesos explícitos do Plano de Ensino quando eles existirem.
- A prova substitutiva (PS) só deve receber peso próprio quando o Plano de Ensino
  trouxer distribuição explícita para ela.
- assignments: lista de trabalhos (K1, K2...) com peso relativo entre 0 e 1.
  Se assignment_weight for 0, retorne []
- TODOS os campos numéricos devem ser números JSON (sem aspas)
- Não use chaves camelCase: use exatamente exam_weight e assignment_weight
- Se um campo obrigatório não for encontrado, retorne null
- NUNCA invente informações que não estejam no texto
- Retorne APENAS o JSON, sem nenhum texto antes ou depois"""


def _bedrock_runtime_client():
    region = os.environ.get("AWS_REGION")
    return boto3.client("bedrock-runtime", region_name=region)


def _extract_content_text(response_body: dict[str, Any]) -> str:
    content_blocks = response_body.get("content", [])
    text_blocks = [
        block.get("text", "")
        for block in content_blocks
        if isinstance(block, dict) and block.get("type") == "text"
    ]
    return "".join(text_blocks).strip()


def _parse_model_json(raw_model_text: str) -> dict[str, Any]:
    """Parse model output, tolerating markdown wrappers around JSON."""
    candidates: list[str] = []

    stripped = raw_model_text.strip()
    if stripped:
        candidates.append(stripped)

    fenced_blocks = re.findall(r"```(?:json)?\s*([\s\S]*?)\s*```", raw_model_text, flags=re.IGNORECASE)
    for block in fenced_blocks:
        block = block.strip()
        if block and block not in candidates:
            candidates.append(block)

    start = raw_model_text.find("{")
    end = raw_model_text.rfind("}")
    if start != -1 and end != -1 and end > start:
        maybe_json = raw_model_text[start : end + 1].strip()
        if maybe_json and maybe_json not in candidates:
            candidates.append(maybe_json)

    last_error: json.JSONDecodeError | None = None
    for candidate in candidates:
        try:
            parsed = json.loads(candidate)
        except json.JSONDecodeError as exc:
            last_error = exc
            continue
        if isinstance(parsed, dict):
            return parsed
        raise ValueError("Bedrock extraction response must be a JSON object")

    if last_error is not None:
        raise last_error
    raise json.JSONDecodeError("No JSON object found in model response", raw_model_text, 0)


def extract_structured_data(text: str) -> dict[str, Any]:
    """Send extracted PDF text to Bedrock and parse the model JSON response."""
    model_id = os.environ.get("BEDROCK_MODEL_ID", DEFAULT_MODEL_ID)
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4096,
        "temperature": 0,
        "system": EXTRACTION_PROMPT,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": text}],
            }
        ],
    }

    logger.info("Invoking Bedrock model %s for plano de ensino extraction", model_id)
    response = _bedrock_runtime_client().invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body).encode("utf-8"),
    )

    raw_body = response["body"].read().decode("utf-8")
    response_body = json.loads(raw_body)
    raw_model_text = _extract_content_text(response_body)

    try:
        parsed = _parse_model_json(raw_model_text)
    except (json.JSONDecodeError, ValueError) as exc:
        logger.error("Bedrock returned invalid JSON. Raw response: %s", raw_model_text)
        raise ValueError("Bedrock returned invalid JSON for plano de ensino extraction") from exc

    return parsed
