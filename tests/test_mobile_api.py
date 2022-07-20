from typing import Dict
from unittest.mock import Mock

import flask
import pytest
from flask.testing import FlaskClient
from flask_batteries_included.helpers import generate_uuid
from pytest_mock import MockFixture

from dhos_telemetry_api.blueprint_api import controller
from dhos_telemetry_api.models.mobile import Mobile


@pytest.mark.usefixtures("mock_bearer_validation")
class TestMobileApi:
    def test_create_telemetry_success(
        self,
        mocker: MockFixture,
        client: FlaskClient,
        mobile_telemetry_in_dict: Dict,
        mobile_telemetry_out_dict: Dict,
    ) -> None:
        """Test creating a mobile installation message"""
        mock_create: Mock = mocker.patch.object(
            controller,
            "create_mobile_installation",
            return_value=mobile_telemetry_out_dict,
        )
        patient_id: str = generate_uuid()
        response = client.post(
            f"/dhos/v1/patient/{patient_id}/installation",
            json=mobile_telemetry_in_dict,
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert mock_create.called_once
        assert response.status_code == 200

    def test_get_patient_installation(
        self,
        mocker: MockFixture,
        client: FlaskClient,
        mobile_telemetry_out_dict: Dict,
    ) -> None:
        mock_get: Mock = mocker.patch.object(
            controller,
            "retrieve_installation_by_id",
            return_value=mobile_telemetry_out_dict,
        )
        patient_id: str = generate_uuid()
        installation_id: str = generate_uuid()
        response = client.get(
            f"/dhos/v1/patient/{patient_id}/installation/{installation_id}",
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 200
        assert response.get_json() == mobile_telemetry_out_dict
        assert mock_get.call_count == 1
        mock_get.assert_called_with(Mobile, patient_id=patient_id, uuid=installation_id)

    def test_get_patient_installation_fails_no_auth(self, client: FlaskClient) -> None:
        response = client.get(f"/dhos/v1/patient/12345/installation/12345")
        assert response.status_code == 401

    def test_get_patient_installation_fails_with_body(
        self, client: FlaskClient
    ) -> None:
        response = client.get(
            f"/dhos/v1/patient/12345/installation/12345",
            json={"something": "here"},
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 400

    def test_patch_patient_installation(
        self, mocker: MockFixture, client: FlaskClient
    ) -> None:
        patient_id: str = generate_uuid()
        installation_id: str = generate_uuid()
        expected_response = {"uuid": installation_id}
        expected_request = {"app_version": "2.0"}
        mock_update: Mock = mocker.patch.object(
            controller, "update_installation", return_value=expected_response
        )
        response = client.patch(
            f"/dhos/v1/patient/{patient_id}/installation/{installation_id}",
            json=expected_request,
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 200
        assert response.json == expected_response
        mock_update.assert_called_with(
            Mobile,
            expected_request,
            patient_id=patient_id,
            uuid=installation_id,
        )

    def test_get_latest_patient_telemetry(
        self,
        mocker: MockFixture,
        client: FlaskClient,
        mobile_telemetry_out_dict: Dict,
    ) -> None:
        mock_get: Mock = mocker.patch.object(
            controller,
            "retrieve_latest_installation",
            return_value=mobile_telemetry_out_dict,
        )
        patient_id: str = generate_uuid()
        response = client.get(
            f"/dhos/v1/patient/{patient_id}/latest_installation",
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 200
        assert response.get_json() == mobile_telemetry_out_dict
        assert mock_get.call_count == 1
        mock_get.assert_called_with(
            Mobile, order_by=Mobile.date_first_launched_, patient_id=patient_id
        )

    def test_get_latest_patient_telemetry_fails_with_body(
        self, client: FlaskClient
    ) -> None:
        response = client.get(
            f"/dhos/v1/patient/12345/latest_installation",
            json={"some": "body"},
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 400
