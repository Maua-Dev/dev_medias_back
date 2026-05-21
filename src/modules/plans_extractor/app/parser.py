import logging
import math
import unicodedata
from typing import Any

from pydantic import ValidationError

from src.shared.domain.entities.disciplina import Disciplina

logger = logging.getLogger(__name__)
LOWERCASE_WORDS = {"a", "as", "da", "das", "de", "do", "dos", "e", "em", "na", "nas", "no", "nos"}
FIRST_SEMESTER_HINTS = ("1 semestre", "1 sem", "primeiro semestre", "semestre 1")
SECOND_SEMESTER_HINTS = ("2 semestre", "2 sem", "segundo semestre", "semestre 2")
SUBSTITUTIVE_HINTS = ("substitutiva", "substitutivo", "substituta", "substituto", "psub", "p sub")


def _to_float(value: Any, default: float = 0.0) -> float:
    if value is None:
        return default
    if isinstance(value, bool):
        raise ValueError("Boolean value is not valid for numeric fields")
    return float(value)


def _normalize_ratio(value: Any, field_name: str) -> float:
    numeric = _to_float(value)
    if numeric < 0:
        raise ValueError(f"{field_name} must be >= 0")
    if numeric > 1:
        if numeric <= 10:
            numeric /= 10
        elif numeric <= 100:
            numeric /= 100
        else:
            raise ValueError(f"{field_name} must be <= 1")
    return numeric


def _normalize_name(value: Any) -> str:
    if value is None:
        return ""

    words = str(value).strip().split()
    if not words:
        return ""

    normalized_words: list[str] = []
    for index, word in enumerate(words):
        lower_word = word.casefold()
        if index > 0 and lower_word in LOWERCASE_WORDS:
            normalized_words.append(lower_word)
        else:
            normalized_words.append(lower_word.capitalize())
    return " ".join(normalized_words)


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


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    normalized = unicodedata.normalize("NFKD", str(value))
    without_accents = "".join(char for char in normalized if not unicodedata.combining(char))
    return " ".join(without_accents.casefold().split())


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


def _truncate_weight(value: float) -> float:
    # Business rule: weights with at most 3 decimal places, without rounding up.
    return math.floor(value * 1000) / 1000


def _truncate_items_weights(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    for item in items:
        item["weight"] = _truncate_weight(item["weight"])
    return items


def _is_substitutive_item(name: Any) -> bool:
    normalized = _normalize_text(name)
    return any(hint in normalized for hint in SUBSTITUTIVE_HINTS)


def _remove_substitutive_items(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [item for item in items if not _is_substitutive_item(item.get("name"))]


def _normalize_items_distribution(
    items: list[dict[str, Any]], fallback_weights: list[float] | None = None
) -> list[dict[str, Any]]:
    if not items:
        return items

    weights = [item["weight"] for item in items]
    has_invalid_weight = any(weight <= 0 for weight in weights)
    weights_sum = sum(weights)
    if has_invalid_weight or weights_sum <= 0:
        if fallback_weights is None:
            fallback_weights = [1 / len(items)] * len(items)
        for index, item in enumerate(items):
            item["weight"] = fallback_weights[index]
        return items

    for item in items:
        item["weight"] = item["weight"] / weights_sum
    return items


def _fallback_exam_weights(count: int, period: str) -> list[float]:
    if count <= 0:
        return []
    if count == 1:
        return [1.0]
    if period == "S":
        # RN CEPE 16/2014 Art. 7 §1: semestral uses simple average.
        return [1 / count] * count
    if count == 2:
        return [0.4, 0.6]

    first_group_count = min(2, count - 1)
    last_group_count = count - first_group_count
    return [0.4 / first_group_count] * first_group_count + [0.6 / last_group_count] * last_group_count


def _semester_bucket(item_name: Any) -> int | None:
    normalized_name = _normalize_text(item_name)
    if any(hint in normalized_name for hint in FIRST_SEMESTER_HINTS):
        return 1
    if any(hint in normalized_name for hint in SECOND_SEMESTER_HINTS):
        return 2
    return None


def _reconcile_annual_semester_split(exams: list[dict[str, Any]], period: str) -> None:
    if period != "A" or len(exams) != 2:
        return

    weights = [item["weight"] for item in exams]
    if not (abs(weights[0] - 0.5) <= 0.01 and abs(weights[1] - 0.5) <= 0.01):
        return

    first_index = None
    second_index = None
    for index, item in enumerate(exams):
        semester = _semester_bucket(item.get("name"))
        if semester == 1 and first_index is None:
            first_index = index
        elif semester == 2 and second_index is None:
            second_index = index

    if first_index is None and second_index is None:
        # Guard-rail fallback: for annual disciplines with exactly two exams and
        # an ambiguous 50/50 split, keep deterministic semester weighting order.
        exams[0]["weight"] = 0.4
        exams[1]["weight"] = 0.6
        return

    if first_index is None and second_index is not None:
        first_index = 1 - second_index
    if second_index is None and first_index is not None:
        second_index = 1 - first_index
    if first_index == second_index:
        exams[0]["weight"] = 0.4
        exams[1]["weight"] = 0.6
        return

    exams[first_index]["weight"] = 0.4
    exams[second_index]["weight"] = 0.6


def _normalize_exams(items: Any, period: str) -> list[dict[str, Any]]:
    normalized_items = _normalize_items(items, "exams")
    normalized_items = _remove_substitutive_items(normalized_items)
    if not normalized_items:
        return []

    fallback = _fallback_exam_weights(len(normalized_items), period)
    normalized_items = _normalize_items_distribution(normalized_items, fallback_weights=fallback)
    _reconcile_annual_semester_split(normalized_items, period)
    return _truncate_items_weights(normalized_items)


def _normalize_assignments(items: Any) -> list[dict[str, Any]]:
    normalized_items = _normalize_items(items, "assignments")
    normalized_items = _remove_substitutive_items(normalized_items)
    if not normalized_items:
        return []
    normalized_items = _normalize_items_distribution(normalized_items)
    return _truncate_items_weights(normalized_items)


def _normalize_assessment_weights(exam_weight: Any, assignment_weight: Any) -> tuple[float, float]:
    normalized_exam_weight = _normalize_ratio(exam_weight, "exam_weight")
    normalized_assignment_weight = _normalize_ratio(assignment_weight, "assignment_weight")
    total = normalized_exam_weight + normalized_assignment_weight

    if total > 0:
        normalized_exam_weight /= total
        normalized_assignment_weight /= total

    return _truncate_weight(normalized_exam_weight), _truncate_weight(normalized_assignment_weight)


def build_disciplina(extracted_data: dict[str, Any], courses: dict[str, int]) -> Disciplina:
    """Validate Bedrock output and add course occurrence data owned by the S3 key."""
    payload = dict(extracted_data)

    payload["name"] = _normalize_name(payload.get("name"))
    payload["period"] = _normalize_period(payload.get("period"))
    raw_exam_weight = payload.get("exam_weight", payload.get("examWeight"))
    raw_assignment_weight = payload.get("assignment_weight", payload.get("assignmentWeight"))
    # Remove alias keys from model output to avoid precedence conflicts
    # during pydantic validation when normalized snake_case fields are set.
    payload.pop("examWeight", None)
    payload.pop("assignmentWeight", None)
    payload["exam_weight"], payload["assignment_weight"] = _normalize_assessment_weights(
        raw_exam_weight,
        raw_assignment_weight,
    )
    payload["exams"] = _normalize_exams(payload.get("exams"), payload["period"])
    payload["assignments"] = _normalize_assignments(payload.get("assignments"))

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
