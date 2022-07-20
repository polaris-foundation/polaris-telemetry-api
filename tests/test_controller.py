import datetime
from typing import Dict

import pytest
from flask_batteries_included.helpers import generate_uuid
from flask_batteries_included.helpers.error_handler import EntityNotFoundException
from flask_batteries_included.sqldb import db
from mock import Mock
from pytest_mock import MockFixture

from dhos_telemetry_api.blueprint_api import controller
from dhos_telemetry_api.models.desktop import Desktop
from dhos_telemetry_api.models.mobile import Mobile


@pytest.mark.usefixtures("app")
class TestController:
    def test_create_clinician_telemetry(
        self, mocker: MockFixture, clinician_telemetry_in_dict: Dict
    ) -> None:
        """Test creating a Clinician installation"""

        clinician_id: str = generate_uuid()
        mock_session_add: Mock = mocker.patch.object(db.session, "add")

        controller.create_desktop_installation(
            clinician_id=clinician_id, installation_data=clinician_telemetry_in_dict
        )

        assert mock_session_add.called_once
        desktop_installation: Desktop = mock_session_add.call_args[0][0]
        installation_to_dict: Dict = desktop_installation.to_dict()

        assert "uuid" in installation_to_dict
        assert installation_to_dict["clinician_id"] == clinician_id
        for k, v in clinician_telemetry_in_dict.items():
            assert installation_to_dict[k] == v

    def test_create_mobile_telemetry(
        self, mocker: MockFixture, mobile_telemetry_in_dict: Dict
    ) -> None:
        """Test creating a Patient installation"""
        patient_id: str = generate_uuid()
        mock_session_add: Mock = mocker.patch.object(db.session, "add")

        controller.create_mobile_installation(
            patient_id=patient_id, installation_data=mobile_telemetry_in_dict
        )

        assert mock_session_add.called_once
        mobile_installation: Mobile = mock_session_add.call_args[0][0]
        installation_to_dict: Dict = mobile_installation.to_dict()

        assert "uuid" in installation_to_dict
        assert installation_to_dict["patient_id"] == patient_id
        for k, v in mobile_telemetry_in_dict.items():
            assert installation_to_dict[k] == v

    def test_retrieve_installation_by_id_success(self) -> None:
        clinician_id: str = generate_uuid()
        installation_id: str = generate_uuid()
        desktop = Desktop(
            uuid=installation_id,
            clinician_id=clinician_id,
            unique_device_code="12345",
            date_first_used="2020-01-01T00:00:00.000Z",
            app_product="GDM",
            app_version="1.0",
            desktop_os="Windows",
            desktop_os_version="10",
            ip_address="1.1.1.1",
        )
        db.session.add(desktop)
        db.session.commit()

        result = controller.retrieve_installation_by_id(
            Desktop, clinician_id=clinician_id, uuid=installation_id
        )
        assert result["uuid"] == installation_id

    def test_retrieve_installation_by_id_failure(self) -> None:
        clinician_id: str = generate_uuid()
        installation_id: str = generate_uuid()

        with pytest.raises(EntityNotFoundException):
            controller.retrieve_installation_by_id(
                Desktop, clinician_id=clinician_id, uuid=installation_id
            )

    def test_retrieve_latest_installation_success(self) -> None:
        patient_id: str = generate_uuid()
        installation_id_1: str = generate_uuid()
        installation_id_2: str = generate_uuid()
        mobile_1 = Mobile(
            uuid=installation_id_1,
            patient_id=patient_id,
            unique_device_code="12345",
            date_first_launched="2020-01-01T00:00:00.000Z",
            app_product="GDM",
            app_version="1.0",
            phone_os="Android",
            phone_os_version="5.0",
            manufacturer="Samsung",
            model="Galaxy",
            display_name="Samsung Galaxy",
        )
        mobile_2 = Mobile(
            uuid=installation_id_2,
            patient_id=patient_id,
            unique_device_code="12345",
            date_first_launched="2020-01-02T00:00:00.000Z",
            app_product="GDM",
            app_version="1.0",
            phone_os="Android",
            phone_os_version="5.0",
            manufacturer="Samsung",
            model="Galaxy",
            display_name="Samsung Galaxy",
        )
        db.session.add(mobile_1)
        db.session.add(mobile_2)
        db.session.commit()

        result = controller.retrieve_latest_installation(
            Mobile, order_by=Mobile.date_first_launched_, patient_id=patient_id
        )
        assert result["uuid"] == installation_id_2

    def test_retrieve_latest_installation_desktop_success(self) -> None:
        now = datetime.datetime.now()
        then = now - datetime.timedelta(seconds=1)

        clinician_id: str = generate_uuid()
        installation_id_1: str = generate_uuid()
        installation_id_2: str = generate_uuid()
        installation_id_3: str = generate_uuid()

        desktop_1 = Desktop(
            uuid=installation_id_1,
            clinician_id=clinician_id,
            unique_device_code="12345",
            date_first_used_=then,
            date_first_used_time_zone_=0,
            app_product="GDM",
            app_version="1.0",
            desktop_os="Windows",
            desktop_os_version="10",
            ip_address="0.0.0.0",
        )
        desktop_2 = Desktop(
            uuid=installation_id_2,
            clinician_id=clinician_id,
            unique_device_code="12345",
            date_first_used_=now,
            date_first_used_time_zone_=0,
            app_product="GDM",
            app_version="1.0",
            desktop_os="Windows",
            desktop_os_version="10",
            ip_address="0.0.0.0",
        )
        desktop_3 = Desktop(
            uuid=installation_id_3,
            clinician_id=clinician_id,
            unique_device_code="12345",
            date_first_used_=now,
            date_first_used_time_zone_=0,
            app_product="GDM",
            app_version="1.1",
            desktop_os="Windows",
            desktop_os_version="10",
            ip_address="0.0.0.0",
        )

        db.session.add(desktop_1)
        db.session.add(desktop_2)
        db.session.add(desktop_3)
        db.session.commit()

        result = controller.retrieve_latest_installation(
            Desktop,
            order_by=(Desktop.date_first_used_, Desktop.app_version),
            clinician_id=clinician_id,
        )

        assert result["uuid"] == installation_id_3

    def test_retrieve_latest_installation_none(self) -> None:
        patient_id: str = generate_uuid()
        result = controller.retrieve_latest_installation(
            Mobile, order_by=Mobile.date_first_launched_, patient_id=patient_id
        )
        assert result == {}

    def test_update_installation(self) -> None:
        clinician_id: str = generate_uuid()
        installation_id: str = generate_uuid()
        desktop = Desktop(
            uuid=installation_id,
            clinician_id=clinician_id,
            unique_device_code="12345",
            date_first_used="2020-01-01T00:00:00.000Z",
            app_product="GDM",
            app_version="1.0",
            desktop_os="Windows",
            desktop_os_version="10",
            ip_address="1.1.1.1",
        )
        db.session.add(desktop)
        db.session.commit()
        result = controller.update_installation(
            Desktop,
            {"app_version": "2.0"},
            clinician_id=clinician_id,
            uuid=installation_id,
        )
        assert result["uuid"] == installation_id
        assert result["app_version"] == "2.0"
