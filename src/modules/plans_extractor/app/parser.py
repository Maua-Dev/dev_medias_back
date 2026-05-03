import logging
from typing import Any

from pydantic import ValidationError

from src.shared.domain.entities.disciplina import Disciplina

logger = logging.getLogger(__name__)


def _to_float(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    if isinstance(value, bool):
        raise ValueError("Boolean value is not valid for numeric fields")
    return float(value)


def _normalize_percentage(value: Any, field_name: str) -> float:
    numeric = _to_float(value)
    if numeric < 0:
        raise ValueError(f"{field_name} must be >= 0")
    if numeric <= 10:
        numeric *= 10
    if numeric > 100:
        raise ValueError(f"{field_name} must be <= 100")
    return numeric


def _normalize_ratio(value: Any, field_name: str) -> float:
    numeric = _to_float(value)
    if numeric < 0:
        raise ValueError(f"{field_name} must be >= 0")
    if numeric > 1:
        if numeric <= 100:
            numeric /= 100
        else:
            raise ValueError(f"{field_name} must be <= 1")
    return numeric


def _normalize_period(value: Any) -> str:
    period_text = "anual" if value is None else str(value).strip().casefold()
    period_map = {
        "s": "S",
        "semestral": "S",
        "semestre": "S",
        "a": "A",
        "anual": "A",
        "ano": "A",
        "t": "T",
        "trimestral": "T",
        "trimestre": "T",
    }
    return period_map.get(period_text, "A")


def _normalize_items(items: Any, field_name: str) -> list[dict[str, Any]]:
    if not items:
        return []
    if not isinstance(items, list):
        raise ValueError(f"{field_name} must be a list")

    normalized_items: list[dict[str, Any]] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValueError(f"{field_name}[{index}] must be an object")
        normalized_items.append(
            {
                "name": item.get("name"),
                "weight": _normalize_ratio(item.get("weight"), f"{field_name}[{index}].weight"),
            }
        )
    return normalized_items


def build_disciplina(extracted_data: dict[str, Any], courses: dict[str, int]) -> Disciplina:
    """Validate Bedrock output and add course occurrence data owned by the S3 key."""
    payload = dict(extracted_data)

    payload["period"] = _normalize_period(payload.get("period"))
    payload["exam_weight"] = _normalize_percentage(payload.get("exam_weight"), "exam_weight")
    payload["assignment_weight"] = _normalize_percentage(payload.get("assignment_weight"), "assignment_weight")
    payload["exams"] = _normalize_items(payload.get("exams"), "exams")
    payload["assignments"] = _normalize_items(payload.get("assignments"), "assignments")

    if payload["exam_weight"] == 0:
        payload["exams"] = []
    if payload["assignment_weight"] == 0:
        payload["assignments"] = []

    # courses is derived from the S3 object name, not from the model output.
    payload["courses"] = courses

    try:
        return Disciplina.model_validate(payload)
    except ValidationError as exc:
        logger.error("Invalid Disciplina payload from Bedrock: %s", exc.errors())
        raise
