"""Pure helpers to force exam/assignment counts from approval criterion codes.

Kept free of AWS/PDF deps so unit tests can run in CI without botocore/pymupdf.
"""

from __future__ import annotations

import logging
import re
from typing import Any

logger = logging.getLogger(__name__)

CRITERION_CODE_REGEX = re.compile(
    r"Crit[eé]rio\s+de\s+aprova[cç][aã]o\s*:\s*([A-E]\d)(?:\s*/\s*\d{4})?",
    re.IGNORECASE,
)
SUBSTITUTIVE_HINTS = (
    "substitutiva",
    "substitutivo",
    "substituta",
    "substituto",
    "psub",
    "p sub",
    "prova sub",
)
# Fallback when criterion includes provas+trabalhos but kp/kt are missing or zero.
DEFAULT_EXAM_WEIGHT = 0.7
DEFAULT_ASSIGNMENT_WEIGHT = 0.3



def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return " ".join(str(value).casefold().split())


def _is_substitutive_name(name: Any) -> bool:
    normalized = _normalize_text(name)
    if not normalized:
        return False
    if normalized in {"ps", "p.s.", "p.s"}:
        return True
    if re.search(r"\bps\b", normalized):
        return True
    return any(hint in normalized for hint in SUBSTITUTIVE_HINTS)


def _numeric_weight(payload: dict[str, Any], *keys: str) -> float:
    for key in keys:
        value = payload.get(key)
        if value is None:
            continue
        try:
            return float(value)
        except (TypeError, ValueError):
            continue
    return 0.0


def extract_criterion_code(criteria_text: str) -> str | None:
    """Extract approval criterion family code (e.g. C4 from 'C4/2015')."""
    if not criteria_text:
        return None
    match = CRITERION_CODE_REGEX.search(criteria_text)
    if not match:
        return None
    return match.group(1).upper()


def determinar_estrutura_provas_trabalhos(
    criterio: str, periodo: str | None = None
) -> tuple[int, bool]:
    """Return definitive `(num_provas, tem_trabalhos)` from criterion family.

    Mapping is authoritative and independent of free-text descriptions in the PDF.
    `periodo` is kept for API compatibility / future E* handling.
    """
    del periodo  # reserved for E* / future rules
    if not criterio:
        raise ValueError("Criterion code is required")

    family = criterio[0].upper()
    digit = criterio[1] if len(criterio) > 1 else ""

    if family == "A":
        return 0, True
    if family == "B":
        if digit == "1":
            return 2, False
        if digit == "2":
            return 4, False
        if digit == "3":
            return 1, False
        return 2, False
    if family == "C":
        if digit == "1":
            return 2, True
        if digit == "2":
            return 4, True
        if digit == "3":
            return 1, True
        # other C* including C4
        return 2, True
    if family == "E":
        # E* keeps model/text-derived structure (special treatment).
        raise ValueError(f"Criterion family E requires specific handling: {criterio}")

    raise ValueError(f"Unknown criterion family: {criterio}")


def apply_criterion_structure(
    extracted_data: dict[str, Any], criteria_text: str
) -> dict[str, Any]:
    """Force exams/assignments counts from the approval criterion code."""
    payload = dict(extracted_data)
    code = extract_criterion_code(criteria_text)
    if code is None:
        logger.warning("No criterion code found in criteria text; skipping structure override")
        return payload

    if code.startswith("E"):
        logger.info("Criterion %s uses specific handling; skipping structure override", code)
        return payload

    period = payload.get("period")
    num_provas, tem_trabalhos = determinar_estrutura_provas_trabalhos(code, period)
    logger.info(
        "Applying criterion %s structure: num_provas=%s tem_trabalhos=%s",
        code,
        num_provas,
        tem_trabalhos,
    )

    existing_exams = payload.get("exams") or []
    if not isinstance(existing_exams, list):
        existing_exams = []
    # Never keep substitutive exams — criterion count is for regular provas only.
    regular_exams = [
        item
        for item in existing_exams
        if isinstance(item, dict) and not _is_substitutive_name(item.get("name"))
    ]

    if num_provas == 0:
        payload["exams"] = []
        payload["examWeight"] = 0
        payload["exam_weight"] = 0
        if _numeric_weight(payload, "assignmentWeight", "assignment_weight") == 0:
            payload["assignmentWeight"] = 1
            payload["assignment_weight"] = 1
    else:
        resized: list[dict[str, Any]] = []
        for index in range(num_provas):
            weight = 0
            if index < len(regular_exams):
                try:
                    weight = float(regular_exams[index].get("weight") or 0)
                except (TypeError, ValueError):
                    weight = 0
            # Canonical names avoid Bedrock "Prova substitutiva"/"PS" surviving into Dynamo.
            resized.append({"name": f"P{index + 1}", "weight": weight})
        payload["exams"] = resized

    if not tem_trabalhos:
        payload["assignments"] = []
        payload["assignmentWeight"] = 0
        payload["assignment_weight"] = 0
        if num_provas > 0 and _numeric_weight(payload, "examWeight", "exam_weight") == 0:
            payload["examWeight"] = 1
            payload["exam_weight"] = 1
    else:
        existing_assignments = payload.get("assignments") or []
        if not isinstance(existing_assignments, list):
            existing_assignments = []
        payload["assignments"] = [
            item
            for item in existing_assignments
            if isinstance(item, dict) and not _is_substitutive_name(item.get("name"))
        ]

    exam_weight = _numeric_weight(payload, "examWeight", "exam_weight")
    assignment_weight = _numeric_weight(payload, "assignmentWeight", "assignment_weight")
    # Bedrock/PDF sometimes return 0/0 (blank kp/kt). Default policy: 70% provas / 30% trabalhos.
    if num_provas > 0 and tem_trabalhos and exam_weight == 0 and assignment_weight == 0:
        payload["examWeight"] = DEFAULT_EXAM_WEIGHT
        payload["exam_weight"] = DEFAULT_EXAM_WEIGHT
        payload["assignmentWeight"] = DEFAULT_ASSIGNMENT_WEIGHT
        payload["assignment_weight"] = DEFAULT_ASSIGNMENT_WEIGHT

    return payload
