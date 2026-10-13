from src.shared.helpers.http.device_id import extract_device_id_header, require_device_id
from src.shared.helpers.errors.controller_errors import MissingParameters
from src.shared.helpers.errors.usecase_errors import InvalidInput
import pytest


def test_extract_case_insensitive():
    assert extract_device_id_header({"X-Device-Id": "abc"}) == "abc"
    assert extract_device_id_header({"x-device-id": "abc"}) == "abc"


def test_require_valid_uuid():
    uid = "550e8400-e29b-41d4-a716-446655440000"
    assert require_device_id({"X-Device-Id": uid}) == uid


def test_require_missing():
    with pytest.raises(MissingParameters):
        require_device_id({})


def test_require_invalid():
    with pytest.raises(InvalidInput):
        require_device_id({"X-Device-Id": "nope"})
