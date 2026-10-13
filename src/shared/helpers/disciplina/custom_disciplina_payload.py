"""Helpers to parse disciplina create/update request bodies (snake_case or camelCase)."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from src.shared.domain.entities.disciplina import Disciplina, ItemAvaliacao
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.usecase_errors import InvalidInput


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _get_field(data: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in data and data[key] is not None:
            return data[key]
    return None


def _require_str(data: dict[str, Any], field_names: tuple[str, ...], canonical: str) -> str:
    value = _get_field(data, *field_names)
    if value is None:
        raise MissingParameters(canonical)
    if not isinstance(value, str):
        raise WrongTypeParameter(
            fieldName=canonical,
            fieldTypeExpected="str",
            fieldTypeReceived=type(value).__name__,
        )
    text = value.strip()
    if not text:
        raise InvalidInput(canonical, "Must not be empty")
    return text


def _optional_str(data: dict[str, Any], field_names: tuple[str, ...], canonical: str) -> str | None:
    value = _get_field(data, *field_names)
    if value is None:
        return None
    if not isinstance(value, str):
        raise WrongTypeParameter(
            fieldName=canonical,
            fieldTypeExpected="str",
            fieldTypeReceived=type(value).__name__,
        )
    text = value.strip()
    return text or None


def _require_number(data: dict[str, Any], field_names: tuple[str, ...], canonical: str) -> float:
    value = _get_field(data, *field_names)
    if value is None:
        raise MissingParameters(canonical)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise WrongTypeParameter(
            fieldName=canonical,
            fieldTypeExpected="float",
            fieldTypeReceived=type(value).__name__,
        )
    return float(value)


def _optional_number(
    data: dict[str, Any], field_names: tuple[str, ...], canonical: str, default: float
) -> float:
    value = _get_field(data, *field_names)
    if value is None:
        return default
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise WrongTypeParameter(
            fieldName=canonical,
            fieldTypeExpected="float",
            fieldTypeReceived=type(value).__name__,
        )
    return float(value)


def _parse_items(raw: Any, field_name: str) -> list[ItemAvaliacao]:
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise WrongTypeParameter(
            fieldName=field_name,
            fieldTypeExpected="list",
            fieldTypeReceived=type(raw).__name__,
        )
    items: list[ItemAvaliacao] = []
    for entry in raw:
        if not isinstance(entry, dict):
            raise InvalidInput(field_name, "Each item must be an object with name and weight")
        name = entry.get("name")
        weight = entry.get("weight")
        if not isinstance(name, str) or not name.strip():
            raise InvalidInput(field_name, "Item name must be a non-empty string")
        if isinstance(weight, bool) or not isinstance(weight, (int, float)):
            raise InvalidInput(field_name, "Item weight must be a number")
        items.append(ItemAvaliacao(name=name.strip(), weight=float(weight)))
    return items


def _parse_courses(raw: Any) -> dict[str, int]:
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise WrongTypeParameter(
            fieldName="courses",
            fieldTypeExpected="dict",
            fieldTypeReceived=type(raw).__name__,
        )
    out: dict[str, int] = {}
    for key, value in raw.items():
        if not isinstance(key, str):
            raise InvalidInput("courses", "Keys must be strings")
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise InvalidInput("courses", "Values must be integers")
        out[key] = int(value)
    return out


def parse_create_disciplina_body(data: dict[str, Any], *, device_id: str) -> Disciplina:
    """Build a custom Disciplina from request body. device_id comes only from header."""
    if not isinstance(data, dict):
        raise InvalidInput("body", "Must be a JSON object")

    # Reject device identity in body — header is the source of truth.
    if _get_field(data, "device_id", "deviceId") is not None:
        raise InvalidInput("device_id", "Must not be sent in body; use X-Device-Id header")

    code = _require_str(data, ("code",), "code")
    name = _require_str(data, ("name",), "name")
    course = _optional_str(data, ("course",), "course") or "CUSTOM"
    period = _optional_str(data, ("period",), "period") or ""
    exam_weight = _optional_number(data, ("exam_weight", "examWeight"), "exam_weight", 0.5)
    assignment_weight = _optional_number(
        data, ("assignment_weight", "assignmentWeight"), "assignment_weight", 0.5
    )
    exams = _parse_items(_get_field(data, "exams"), "exams")
    assignments = _parse_items(_get_field(data, "assignments"), "assignments")
    courses = _parse_courses(_get_field(data, "courses"))
    exams_code = _optional_str(data, ("exams_code", "examsCode"), "exams_code")
    # Custom subjects never get catalog PDF URLs from the client.
    now = utc_now_iso()

    return Disciplina(
        course=course,
        name=name,
        code=code,
        period=period,
        exam_weight=exam_weight,
        assignment_weight=assignment_weight,
        exams=exams,
        assignments=assignments,
        courses=courses,
        study_plan_download_pdf_url=None,
        exams_code=exams_code,
        device_id=device_id,
        is_custom=True,
        created_at=now,
        updated_at=now,
    )


def parse_update_disciplina_body(
    data: dict[str, Any],
    *,
    existing: Disciplina,
    device_id: str,
) -> Disciplina:
    """Merge partial/full update onto an existing custom disciplina."""
    if not isinstance(data, dict):
        raise InvalidInput("body", "Must be a JSON object")

    if _get_field(data, "device_id", "deviceId") is not None:
        raise InvalidInput("device_id", "Must not be sent in body; use X-Device-Id header")

    code_in_body = _get_field(data, "code")
    if code_in_body is not None and str(code_in_body).strip() != existing.code:
        raise InvalidInput("code", "Cannot change code; delete and recreate instead")

    name = (
        _require_str(data, ("name",), "name")
        if _get_field(data, "name") is not None
        else existing.name
    )
    course = (
        _require_str(data, ("course",), "course")
        if _get_field(data, "course") is not None
        else existing.course
    )
    period = (
        _optional_str(data, ("period",), "period")
        if ("period" in data)
        else existing.period
    )
    if period is None:
        period = existing.period

    exam_weight = (
        _require_number(data, ("exam_weight", "examWeight"), "exam_weight")
        if _get_field(data, "exam_weight", "examWeight") is not None
        else existing.exam_weight
    )
    assignment_weight = (
        _require_number(data, ("assignment_weight", "assignmentWeight"), "assignment_weight")
        if _get_field(data, "assignment_weight", "assignmentWeight") is not None
        else existing.assignment_weight
    )

    exams = (
        _parse_items(_get_field(data, "exams"), "exams")
        if "exams" in data
        else list(existing.exams)
    )
    assignments = (
        _parse_items(_get_field(data, "assignments"), "assignments")
        if "assignments" in data
        else list(existing.assignments)
    )
    courses = (
        _parse_courses(_get_field(data, "courses"))
        if "courses" in data
        else dict(existing.courses)
    )
    exams_code = (
        _optional_str(data, ("exams_code", "examsCode"), "exams_code")
        if ("exams_code" in data or "examsCode" in data)
        else existing.exams_code
    )

    return Disciplina(
        course=course,
        name=name,
        code=existing.code,
        period=period or "",
        exam_weight=exam_weight,
        assignment_weight=assignment_weight,
        exams=exams,
        assignments=assignments,
        courses=courses,
        study_plan_download_pdf_url=None,
        exams_code=exams_code,
        device_id=device_id,
        is_custom=True,
        created_at=existing.created_at,
        updated_at=utc_now_iso(),
    )


def resolve_code_from_request(data: dict[str, Any], query_params: dict[str, Any] | None) -> str:
    """code from body or query string (path-style resources not used in this IaC)."""
    value = _get_field(data or {}, "code")
    if value is None and query_params:
        value = query_params.get("code")
    if value is None:
        raise MissingParameters("code")
    if not isinstance(value, str):
        raise WrongTypeParameter(
            fieldName="code",
            fieldTypeExpected="str",
            fieldTypeReceived=type(value).__name__,
        )
    text = value.strip()
    if not text:
        raise InvalidInput("code", "Must not be empty")
    return text
