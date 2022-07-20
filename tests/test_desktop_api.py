from typing import Dict
from unittest.mock import Mock

import pytest
from flask.testing import FlaskClient
from flask_batteries_included.helpers import generate_uuid
from pytest_mock import MockFixture

from dhos_telemetry_api.blueprint_api import controller
from dhos_telemetry_api.models.desktop import Desktop


@pytest.mark.usefixtures("mock_bearer_validation")
class TestDesktopApi:
    def test_create_telemetry_success(
        self,
        mocker: MockFixture,
        client: FlaskClient,
        clinician_telemetry_in_dict: Dict,
        clinician_telemetry_out_dict: Dict,
    ) -> None:
        """Test creating a Clinician installation"""
        mock_create: Mock = mocker.patch.object(
            controller,
            "create_desktop_installation",
            return_value=clinician_telemetry_out_dict,
        )
        clinician_id: str = generate_uuid()
        response = client.post(
            f"/dhos/v1/clinician/{clinician_id}/installation",
            json=clinician_telemetry_in_dict,
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert mock_create.called_once
        assert response.status_code == 200

    def test_create_telemetry_failure(
        self,
        mocker: MockFixture,
        client: FlaskClient,
        clinician_telemetry_in_dict: Dict,
    ) -> None:
        """Test creating a Clinician installation"""
        mock_create: Mock = mocker.patch.object(
            controller, "create_desktop_installation"
        )
        clinician_id: str = generate_uuid()
        response = client.post(
            f"/dhos/v1/clinician/{clinician_id}/installation",
            json={**clinician_telemetry_in_dict, "wrong": "key"},
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert mock_create.called_once
        assert response.status_code == 400

    def test_create_telemetry_failure_no_body(
        self,
        client: FlaskClient,
    ) -> None:
        response = client.post(
            f"/dhos/v1/clinician/12345/installation",
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 400

    def test_get_clinician_telemetry_by_id_success(
        self,
        mocker: MockFixture,
        client: FlaskClient,
        clinician_telemetry_out_dict: Dict,
    ) -> None:
        """Test retrieving a Clinician installation message"""
        mock_create: Mock = mocker.patch.object(
            controller,
            "retrieve_installation_by_id",
            return_value=clinician_telemetry_out_dict,
        )
        clinician_id: str = generate_uuid()
        installation_id: str = generate_uuid()
        response = client.get(
            f"/dhos/v1/clinician/{clinician_id}/installation/{installation_id}",
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert mock_create.called_once
        assert response.status_code == 200
        assert response.get_json() == clinician_telemetry_out_dict

    def test_get_clinician_telemetry_by_id_failure(
        self, mocker: MockFixture, client: FlaskClient
    ) -> None:
        """Test retrieving a nonexistent Clinician installation"""
        mock_create: Mock = mocker.patch.object(
            controller, "retrieve_installation_by_id", return_value={}
        )
        clinician_id: str = generate_uuid()
        installation_id: str = generate_uuid()
        response = client.get(
            f"/dhos/v1/clinician/{clinician_id}/installation/{installation_id}",
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert mock_create.called_once
        assert response.status_code == 200
        assert response.get_json() == {}

    def test_get_clinician_telemetry_by_id_failure_with_body(
        self, client: FlaskClient
    ) -> None:
        response = client.get(
            f"/dhos/v1/clinician/12345/installation/12345",
            json={"some": "body"},
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 400

    def test_get_clinician_telemetry_by_latest_success(
        self,
        mocker: MockFixture,
        client: FlaskClient,
        clinician_telemetry_out_dict: Dict,
    ) -> None:
        """Test retrieving the latest Clinician installation"""
        mock_create: Mock = mocker.patch.object(
            controller,
            "retrieve_latest_installation",
            return_value=clinician_telemetry_out_dict,
        )
        clinician_id: str = generate_uuid()
        response = client.get(
            f"/dhos/v1/clinician/{clinician_id}/latest_installation",
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert mock_create.called_once
        assert response.status_code == 200
        assert response.get_json() == clinician_telemetry_out_dict

    def test_get_clinician_telemetry_by_latest_failure(
        self, mocker: MockFixture, client: FlaskClient
    ) -> None:
        """Test retrieving the latest Clinician installation message with no results"""
        mock_create: Mock = mocker.patch.object(
            controller, "retrieve_latest_installation", return_value={}
        )
        clinician_id: str = generate_uuid()
        response = client.get(
            f"/dhos/v1/clinician/{clinician_id}/latest_installation",
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert mock_create.called_once
        assert response.status_code == 200
        assert response.get_json() == {}

    def test_get_clinician_telemetry_by_latest_failure_with_body(
        self, client: FlaskClient
    ) -> None:
        response = client.get(
            f"/dhos/v1/clinician/12345/latest_installation",
            json={"some": "body"},
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 400

    def test_patch_clinician_installation(
        self, mocker: MockFixture, client: FlaskClient
    ) -> None:
        clinician_id: str = generate_uuid()
        installation_id: str = generate_uuid()
        expected_response = {"uuid": installation_id}
        expected_request = {"app_version": "2.0"}
        mock_update: Mock = mocker.patch.object(
            controller, "update_installation", return_value=expected_response
        )
        response = client.patch(
            f"/dhos/v1/clinician/{clinician_id}/installation/{installation_id}",
            json=expected_request,
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 200
        assert response.json == expected_response
        mock_update.assert_called_with(
            Desktop,
            expected_request,
            clinician_id=clinician_id,
            uuid=installation_id,
        )
