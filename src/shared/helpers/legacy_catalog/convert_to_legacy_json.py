"""Convert Academic Catalog Dynamo items → legacy allSubjects / courses JSON.

Ported from ``tmp_export/convert_dynamo_to_legacy_json.py`` for reuse by CLI and Lambda.
"""

from __future__ import annotations

import re
import unicodedata
from collections import Counter
from typing import Any

SUBSTITUTIVE_HINTS = (
    "substitutiva",
    "substitutivo",
    "substituta",
    "substituto",
    "psub",
    "p sub",
    "prova sub",
)

ORDINAL_PT = {
    "primeira": 1,
    "primeiro": 1,
    "1": 1,
    "1o": 1,
    "1º": 1,
    "segunda": 2,
    "segundo": 2,
    "2": 2,
    "2o": 2,
    "2º": 2,
    "terceira": 3,
    "terceiro": 3,
    "3": 3,
    "3o": 3,
    "3º": 3,
    "quarta": 4,
    "quarto": 4,
    "4": 4,
    "4o": 4,
    "4º": 4,
    "quinta": 5,
    "quinto": 5,
    "5": 5,
    "5o": 5,
    "5º": 5,
    "sexta": 6,
    "sexto": 6,
    "6": 6,
    "6o": 6,
    "6º": 6,
    "setima": 7,
    "sétima": 7,
    "setimo": 7,
    "sétimo": 7,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
}

EXPLICIT_CODE_RE = re.compile(r"(?i)\b(ps|p|t|k)(\d{1,2})\b")
NUMBERED_ITEM_RE = re.compile(
    r"(?i)\b(?:prova|trabalho|avaliacao|avaliação|atividade|projeto|exercicio|exercício)\s*"
    r"(?:n[ºo°.]?\s*)?(\d{1,2})\b"
)


def unmarshall_value(value: Any) -> Any:
    if not isinstance(value, dict):
        return value
    if "S" in value:
        return value["S"]
    if "N" in value:
        return float(value["N"])
    if "BOOL" in value:
        return value["BOOL"]
    if "NULL" in value:
        return None
    if "L" in value:
        return [unmarshall_value(item) for item in value["L"]]
    if "M" in value:
        return {key: unmarshall_value(item) for key, item in value["M"].items()}
    return {key: unmarshall_value(item) for key, item in value.items()}


def unmarshall_item(item: dict[str, Any]) -> dict[str, Any]:
    return {key: unmarshall_value(value) for key, value in item.items()}


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    normalized = unicodedata.normalize("NFKD", str(value))
    without_accents = "".join(char for char in normalized if not unicodedata.combining(char))
    return " ".join(without_accents.casefold().split())


def is_substitutive(name: Any) -> bool:
    text = normalize_text(name)
    return any(hint in text for hint in SUBSTITUTIVE_HINTS)


def to_percent(weight: Any) -> float:
    """Legacy allSubjects uses examWeight/assignmentWeight on a 0–100 scale."""
    numeric = float(weight or 0.0)
    if numeric < 0:
        numeric = 0.0
    if numeric <= 1.0:
        return round(numeric * 100.0, 1)
    if numeric <= 100.0:
        return round(numeric, 1)
    return round(numeric, 1)


def to_ratio(weight: Any) -> float:
    numeric = float(weight or 0.0)
    if numeric < 0:
        return 0.0
    if numeric > 1:
        if numeric <= 10:
            numeric /= 10.0
        elif numeric <= 100:
            numeric /= 100.0
    return round(numeric, 3)


def extract_explicit_code(name: Any) -> str | None:
    match = EXPLICIT_CODE_RE.search(str(name or ""))
    if not match:
        return None
    prefix, number = match.group(1).upper(), int(match.group(2))
    if prefix == "PS":
        prefix = "P"
    return f"{prefix}{number}"


def extract_ordinal(name: Any) -> int | None:
    text = normalize_text(name)
    for token, number in ORDINAL_PT.items():
        patterns = (
            rf"\b{re.escape(token)}\b.*\b(prova|avaliacao|trabalho|atividade|projeto)\b",
            rf"\b(prova|avaliacao|trabalho|atividade|projeto)\b.*\b{re.escape(token)}\b",
            rf"\b{re.escape(token)}\b\s+(bimestre|semestre|periodo)",
            rf"\b(bimestre|semestre|periodo)\s+{re.escape(token)}\b",
        )
        if any(re.search(pattern, text) for pattern in patterns):
            return number

    numbered = NUMBERED_ITEM_RE.search(str(name or ""))
    if numbered:
        return int(numbered.group(1))
    return None


def allocate_codes(
    items: list[dict[str, Any]],
    *,
    kind: str,
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    """Map descriptive names → short legacy keys (P# / T# / K#)."""
    default_prefix = "P" if kind == "exam" else "T"
    used: set[str] = set()
    output: list[dict[str, Any]] = []
    renames: list[dict[str, str]] = []

    def next_free(prefix: str, preferred: int | None = None) -> str:
        start = preferred if preferred and preferred > 0 else 1
        candidate = start
        while f"{prefix}{candidate}" in used:
            candidate += 1
        return f"{prefix}{candidate}"

    for item in items:
        original = str(item.get("name") or "").strip()
        weight = to_ratio(item.get("weight"))

        explicit = extract_explicit_code(original)
        ordinal = extract_ordinal(original)

        if explicit:
            number = int(explicit[1:])
            if kind == "exam":
                prefix = "P"
            else:
                prefix = explicit[0]
                if prefix not in {"T", "K"}:
                    prefix = default_prefix
            preferred = f"{prefix}{number}"
            code = preferred if preferred not in used else next_free(prefix, number)
        elif ordinal is not None:
            code = next_free(default_prefix, ordinal)
        else:
            code = next_free(default_prefix)

        used.add(code)
        output.append({"name": code, "weight": weight})
        if code != original:
            renames.append({"from": original, "to": code})

    return output, renames


def convert_disciplina(raw: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    code = str(raw.get("code") or "").strip()
    exams_raw = [item for item in (raw.get("exams") or []) if isinstance(item, dict)]
    assigns_raw = [item for item in (raw.get("assignments") or []) if isinstance(item, dict)]

    exams_raw = [item for item in exams_raw if not is_substitutive(item.get("name"))]
    assigns_raw = [item for item in assigns_raw if not is_substitutive(item.get("name"))]

    exam_weight = to_percent(raw.get("exam_weight", raw.get("examWeight")))
    assignment_weight = to_percent(raw.get("assignment_weight", raw.get("assignmentWeight")))

    if exam_weight == 0:
        exams_raw = []
    if assignment_weight == 0:
        assigns_raw = []

    exams, exam_renames = allocate_codes(exams_raw, kind="exam")
    assignments, assign_renames = allocate_codes(assigns_raw, kind="assignment")

    courses: dict[str, int] = {}
    for course_code, year in (raw.get("courses") or {}).items():
        key = str(course_code).strip().upper()
        if key == "UNK":
            key = "ECO"
        courses[key] = int(float(year))

    subject = {
        "course": str(raw.get("course") or ""),
        "name": str(raw.get("name") or ""),
        "code": code,
        "period": str(raw.get("period") or "A"),
        "examWeight": exam_weight,
        "assignmentWeight": assignment_weight,
        "exams": exams,
        "assignments": assignments,
        "courses": courses,
    }

    meta = {
        "code": code,
        "exam_renames": exam_renames,
        "assignment_renames": assign_renames,
        "dropped_substitutive_exams": [
            item.get("name")
            for item in (raw.get("exams") or [])
            if isinstance(item, dict) and is_substitutive(item.get("name"))
        ],
        "dropped_substitutive_assignments": [
            item.get("name")
            for item in (raw.get("assignments") or [])
            if isinstance(item, dict) and is_substitutive(item.get("name"))
        ],
    }
    return subject, meta


def convert_curso(raw: dict[str, Any]) -> tuple[str, str]:
    code = str(raw.get("código") or raw.get("codigo") or raw.get("code") or "").strip()
    name = str(raw.get("nome") or raw.get("name") or "").strip()
    return code, name


def is_global_catalog_item(item: dict[str, Any]) -> bool:
    """Keep only GLOBAL#… rows (skip user-owned custom disciplinas/cursos)."""
    pk = str(item.get("pk") or "")
    return pk.startswith("GLOBAL#")


def should_export_disciplina(item: dict[str, Any]) -> bool:
    if not is_global_catalog_item(item):
        return False
    if item.get("is_custom") is True:
        return False
    return True


def build_legacy_catalog(
    items: list[dict[str, Any]],
    *,
    items_are_attribute_values: bool = False,
) -> tuple[dict[str, Any], dict[str, str], dict[str, Any]]:
    """Return ``(all_subjects, courses, report_meta)`` from Dynamo items."""
    all_subjects: dict[str, Any] = {}
    courses: dict[str, str] = {}
    rename_log: list[dict[str, Any]] = []
    skipped_custom = 0

    for raw in items:
        item = unmarshall_item(raw) if items_are_attribute_values else raw
        entity = item.get("entity_type")
        if entity == "DISCIPLINA":
            if not should_export_disciplina(item):
                skipped_custom += 1
                continue
            subject, meta = convert_disciplina(item)
            code = subject["code"]
            if not code:
                continue
            all_subjects[code] = subject
            if meta["exam_renames"] or meta["assignment_renames"]:
                rename_log.append(meta)
        elif entity == "CURSO":
            if not is_global_catalog_item(item):
                continue
            code, name = convert_curso(item)
            if code:
                courses[code] = name

    all_subjects = dict(sorted(all_subjects.items()))
    courses = dict(sorted(courses.items()))

    exam_names: Counter[str] = Counter()
    assign_names: Counter[str] = Counter()
    for subject in all_subjects.values():
        for exam in subject.get("exams") or []:
            exam_names[str(exam.get("name") or "")] += 1
        for assignment in subject.get("assignments") or []:
            assign_names[str(assignment.get("name") or "")] += 1

    report_meta = {
        "subjects_count": len(all_subjects),
        "courses_count": len(courses),
        "skipped_non_global_or_custom": skipped_custom,
        "renamed_subjects_count": len(rename_log),
        "exam_names": dict(exam_names.most_common()),
        "assignment_names": dict(assign_names.most_common()),
    }
    return all_subjects, courses, report_meta
