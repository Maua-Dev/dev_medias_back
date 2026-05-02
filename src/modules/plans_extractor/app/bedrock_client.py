import json
import logging
import os
from typing import Any

import boto3

logger = logging.getLogger(__name__)

DEFAULT_MODEL_ID = "anthropic.claude-haiku-4-5-20251001-v1:0"

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
- name: valor do campo "Disciplina" em português, em caixa alta
- course: valor do campo "Materia" em português. Se vazio, use "Disciplina".
  Nunca use o campo "Course" (inglês) nem "TEMÁRIO" (espanhol)
- period: procure "semestral", "anual", "trimestral" nas seções de Avaliação
  e Outras Informações. Se não encontrar, retorne "anual"
- exam_weight: campo "Peso de MP (kp)". Se ausente, retorne 0
- assignment_weight: campo "Peso de MT (kt)". Se ausente, retorne 0
- exams: provas P1, P2, PS com peso 1.0 cada. Se exam_weight for 0, retorne []
- assignments: trabalhos K1, K2... com seus valores numéricos como peso.
  Se assignment_weight for 0, retorne []
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
        parsed = json.loads(raw_model_text)
    except json.JSONDecodeError as exc:
        logger.error("Bedrock returned invalid JSON. Raw response: %s", raw_model_text)
        raise ValueError("Bedrock returned invalid JSON for plano de ensino extraction") from exc

    if not isinstance(parsed, dict):
        logger.error("Bedrock returned a non-object JSON payload: %s", raw_model_text)
        raise ValueError("Bedrock extraction response must be a JSON object")

    return parsed
