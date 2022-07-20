from typing import Dict, Generator

import pytest
from flask import Flask
from mock import Mock
from pytest_mock import MockFixture


@pytest.fixture()
def app() -> Flask:
    """ "Fixture that creates app for testing"""
    from dhos_telemetry_api.app import create_app

    return create_app(testing=True, use_pgsql=False, use_sqlite=True)


@pytest.fixture
def app_context(app: Flask) -> Generator[None, None, None]:
    with app.app_context():
        yield


@pytest.fixture
def mock_bearer_validation(mocker: MockFixture) -> Mock:
    from jose import jwt

    mocked = mocker.patch.object(jwt, "get_unverified_claims")
    mocked.return_value = {
        "sub": "1234567890",
        "name": "John Doe",
        "iat": 1_516_239_022,
        "iss": "http://localhost/",
    }
    return mocked


@pytest.fixture
def clinician_telemetry_in_dict() -> Dict:
    """Sample Clinician telemetry to post in"""
    return {
        "unique_device_code": "0987654321",
        "date_first_used": "1970-01-01T00:00:00.000Z",
        "app_product": "GDM",
        "app_version": "18.1.x",
        "desktop_os": "windows",
        "desktop_os_version": "2001",
        "ip_address": "195.189.79.280",
    }


@pytest.fixture
def clinician_telemetry_out_dict(clinician_telemetry_in_dict: Dict) -> Dict:
    """Sample Clinician telemetry to post in"""
    return {
        "uuid": "12345",
        "created_by": "test_user",
        "updated_by": "test_user",
        **clinician_telemetry_in_dict,
    }


@pytest.fixture
def mobile_telemetry_in_dict() -> Dict:
    return {
        "unique_device_code": "0987654321",
        "date_first_launched": "1970-01-01T00:00:00.000Z",
        "app_product": "GDM",
        "app_version": "18.1.x",
        "phone_os": "android",
        "phone_os_version": "v9001",
        "manufacturer": "phoneCo",
        "model": "TheGoodOne",
        "display_name": "phoneCo TheGoodOne",
    }


@pytest.fixture
def mobile_telemetry_out_dict(mobile_telemetry_in_dict: Dict) -> Dict:
    """Sample Clinician telemetry to post in"""
    return {
        "uuid": "12345",
        "created_by": "test_user",
        "updated_by": "test_user",
        **mobile_telemetry_in_dict,
    }


@pytest.fixture
def meter_in_dict() -> Dict:
    return {
        "mobile_id": "0987654321",
        "serial_number": "SN132654",
        "date_verified": "2021-01-01T00:00:00.000Z",
        "is_bg_value_correct": True,
        "app_version": "19.1.54",
        "blood_glucose_value": 5.5,
        "app_product": "GDM",
    }


@pytest.fixture
def meter_out_dict(meter_in_dict: Dict) -> Dict:
    return {
        "uuid": "bfa9aa4b-a730-4ea1-bc87-b9522ffdbffd",
        "created_by": "test_user",
        "modified_by": "test_user",
        "patient_id": "f56c4b03-1f4f-4c7f-97c2-e9bdcc4b3922",
        "app_product": "GDM",
        **meter_in_dict,
    }
