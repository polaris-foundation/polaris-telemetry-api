from typing import Dict
from unittest.mock import Mock

import flask
import pytest
from flask.testing import FlaskClient
from flask_batteries_included.helpers import generate_uuid
from pytest_mock import MockFixture

from dhos_telemetry_api.blueprint_api import controller
from dhos_telemetry_api.models.blood_glucose_meter import BloodGlucoseMeter


@pytest.mark.usefixtures("mock_bearer_validation")
class TestMeterApi:
    def test_create_meter_success(
        self,
        mocker: MockFixture,
        client: FlaskClient,
        meter_in_dict: Dict,
        meter_out_dict: Dict,
    ) -> None:
        """Test creating a mobile installation message"""
        mock_create: Mock = mocker.patch.object(
            controller,
            "create_blood_glucose_meter",
            return_value=meter_out_dict,
        )
        response = client.post(
            f"/dhos/v1/patient/f56c4b03-1f4f-4c7f-97c2-e9bdcc4b3922/blood_glucose_meter",
            json=meter_in_dict,
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert mock_create.called_once
        assert response.status_code == 201

    def test_patch_meter(self, mocker: MockFixture, client: FlaskClient) -> None:
        uuid: str = generate_uuid()
        patient_id: str = generate_uuid()
        expected_response = {"uuid": uuid}
        expected_request = {"app_version": "2.0"}
        mock_update: Mock = mocker.patch.object(
            controller, "update_blood_glucose_meter", return_value=expected_response
        )
        response = client.patch(
            f"/dhos/v1/patient/{patient_id}/blood_glucose_meter/{uuid}",
            json=expected_request,
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 200
        assert response.json == expected_response
        mock_update.assert_called_with(
            patient_id=patient_id,
            meter_id=uuid,
            update_data=expected_request,
        )

    def test_get_meter(
        self,
        mocker: MockFixture,
        client: FlaskClient,
        meter_out_dict: Dict,
    ) -> None:
        mock_get: Mock = mocker.patch.object(
            controller,
            "get_blood_glucose_meter",
            return_value=meter_out_dict,
        )
        uuid: str = generate_uuid()
        patient_id: str = generate_uuid()
        response = client.get(
            f"/dhos/v1/patient/{patient_id}/blood_glucose_meter/{uuid}",
            headers={"Authorization": "Bearer TOKEN"},
        )
        assert response.status_code == 200
        assert response.get_json() == meter_out_dict
        assert mock_get.call_count == 1
        mock_get.assert_called_with(patient_id=patient_id, meter_id=uuid)
