import logging
from typing import Any

from pydantic import ValidationError

from src.shared.domain.entities.disciplina import Disciplina

logger = logging.getLogger(__name__)


def build_disciplina(extracted_data: dict[str, Any], courses: dict[str, int]) -> Disciplina:
    """Validate Bedrock output and add course occurrence data owned by the S3 key."""
    payload = dict(extracted_data)

    if payload.get("period") is None:
        logger.warning("Bedrock returned null period; defaulting to anual")
        payload["period"] = "anual"

    # courses is derived from the S3 object name, not from the model output.
    payload["courses"] = courses

    try:
        return Disciplina.model_validate(payload)
    except ValidationError as exc:
        logger.error("Invalid Disciplina payload from Bedrock: %s", exc.errors())
        raise
