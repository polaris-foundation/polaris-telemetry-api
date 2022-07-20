from typing import Any, Collection, Dict, Type, Union

from flask_batteries_included.helpers import generate_uuid
from flask_batteries_included.helpers.error_handler import EntityNotFoundException
from flask_batteries_included.sqldb import db
from she_logging import logger

from dhos_telemetry_api.models.blood_glucose_meter import BloodGlucoseMeter
from dhos_telemetry_api.models.desktop import Desktop
from dhos_telemetry_api.models.mobile import Mobile


def retrieve_installation_by_id(
    model: Union[Type[Desktop], Type[Mobile]], **kwargs: Any
) -> Dict:

    installation = model.query.filter_by(**kwargs).first()

    if installation:
        return installation.to_dict()
    else:
        raise EntityNotFoundException()


def retrieve_latest_installation(
    model: Union[Type[Desktop], Type[Mobile]], order_by: Any, **kwargs: Any
) -> Dict:

    query = model.query.filter_by(**kwargs)

    if isinstance(order_by, Collection):
        for order in order_by:
            query = query.order_by(order.desc())
    else:
        query = query.order_by(order_by.desc())

    installation = query.first()

    if installation:
        return installation.to_dict()
    else:
        return {}


def update_installation(
    model: Union[Type[Desktop], Type[Mobile]], update_data: Dict, **kwargs: Any
) -> Dict:

    installation = model.query.filter_by(**kwargs).first_or_404()

    for key in update_data:
        setattr(installation, key, update_data[key])

    db.session.commit()

    return installation.to_dict()


def create_mobile_installation(patient_id: str, installation_data: Dict) -> Dict:
    logger.debug("Creating mobile installation for patient %s", patient_id)

    unique_device_code = installation_data.pop("unique_device_code")
    date_first_launched = installation_data.pop("date_first_launched")
    app_product = installation_data.pop("app_product")
    app_version = installation_data.pop("app_version")
    phone_os = installation_data.pop("phone_os")
    phone_os_version = installation_data.pop("phone_os_version")
    manufacturer = installation_data.pop("manufacturer")
    model = installation_data.pop("model")
    display_name = installation_data.pop("display_name")

    # Create installation
    mobile = Mobile(
        uuid=generate_uuid(),
        patient_id=patient_id,
        unique_device_code=unique_device_code,
        date_first_launched=date_first_launched,
        app_product=app_product,
        app_version=app_version,
        phone_os=phone_os,
        phone_os_version=phone_os_version,
        manufacturer=manufacturer,
        model=model,
        display_name=display_name,
    )

    db.session.add(mobile)
    db.session.flush()
    db.session.commit()

    return mobile.to_dict()


def create_desktop_installation(clinician_id: str, installation_data: Dict) -> Dict:
    logger.debug("Creating desktop installation for clinician %s", clinician_id)

    unique_device_code = installation_data.pop("unique_device_code")
    date_first_used = installation_data.pop("date_first_used")
    app_product = installation_data.pop("app_product")
    app_version = installation_data.pop("app_version")
    desktop_os = installation_data.pop("desktop_os")
    desktop_os_version = installation_data.pop("desktop_os_version")
    ip_address = installation_data.pop("ip_address")

    # Create installation
    desktop = Desktop(
        uuid=generate_uuid(),
        clinician_id=clinician_id,
        unique_device_code=unique_device_code,
        date_first_used=date_first_used,
        app_product=app_product,
        app_version=app_version,
        desktop_os=desktop_os,
        desktop_os_version=desktop_os_version,
        ip_address=ip_address,
    )

    db.session.add(desktop)
    db.session.flush()
    db.session.commit()

    return desktop.to_dict()


def create_blood_glucose_meter(patient_id: str, meter_data: Dict) -> Dict:
    logger.debug("Creating blood glucose meter for patient %s", patient_id)
    meter = BloodGlucoseMeter(
        uuid=generate_uuid(),
        patient_id=patient_id,
        mobile_id=meter_data.get("mobile_id"),
        serial_number=meter_data.get("serial_number"),
        date_verified=meter_data.get("date_verified"),
        is_bg_value_correct=meter_data.get("is_bg_value_correct"),
        app_version=meter_data.get("app_version"),
        app_product=meter_data.get("app_product"),
        blood_glucose_value=meter_data.get("blood_glucose_value"),
    )

    db.session.add(meter)
    db.session.commit()

    return meter.to_dict()


def update_blood_glucose_meter(
    meter_id: str, patient_id: str, update_data: Dict
) -> Dict:
    logger.debug("Updating blood glucose meter for patient %s", patient_id)
    meter = BloodGlucoseMeter.query.filter_by(
        uuid=meter_id, patient_id=patient_id
    ).first_or_404()
    for key in update_data:
        setattr(meter, key, update_data[key])

    db.session.commit()

    return meter.to_dict()


def get_blood_glucose_meter(meter_id: str, patient_id: str) -> Dict:
    logger.debug("Getting blood glucose meter for patient %s", patient_id)
    meter = BloodGlucoseMeter.query.filter_by(
        uuid=meter_id, patient_id=patient_id
    ).first_or_404()
    return meter.to_dict()
