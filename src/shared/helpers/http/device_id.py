"""Helpers for device-scoped custom disciplinas (header X-Device-Id)."""

from __future__ import annotations

import re
from typing import Any, Mapping

from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.usecase_errors import InvalidInput

DEVICE_ID_HEADER = "x-device-id"
_UUID_RE = re.compile(
    r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
)


def extract_device_id_header(headers: Mapping[str, Any] | None) -> str | None:
    if not headers:
        return None
    for key, value in headers.items():
        if str(key).lower() == DEVICE_ID_HEADER:
            if value is None:
                return None
            text = str(value).strip()
            return text or None
    return None


def require_device_id(headers: Mapping[str, Any] | None) -> str:
    """Return validated device UUID or raise 400-class errors."""
    device_id = extract_device_id_header(headers)
    if device_id is None:
        raise MissingParameters("X-Device-Id")
    if not _UUID_RE.match(device_id):
        raise InvalidInput("X-Device-Id", "Must be a UUID")
    return device_id
