from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask_batteries_included.helpers.apispec import (
    FlaskBatteriesPlugin,
    Identifier,
    initialise_apispec,
    openapi_schema,
)
from marshmallow import EXCLUDE, Schema, fields

dhos_telemetry_api_spec: APISpec = APISpec(
    version="1.0.0",
    openapi_version="3.0.3",
    title="DHOS Telemetry API",
    info={
        "description": "The DHOS Telemetry API is responsible for storing and retrieving information about user installations."
    },
    plugins=[FlaskPlugin(), MarshmallowPlugin(), FlaskBatteriesPlugin()],
)

initialise_apispec(dhos_telemetry_api_spec)


class SharedInstallationSchema(Schema):
    class Meta:
        ordered = True

    app_product = fields.String(
        required=True,
        metadata={"description": "Product name for the installation", "example": "GDM"},
    )

    app_version = fields.String(
        required=True,
        metadata={"description": "Version string of app", "example": "v19.1.31"},
    )


class SharedInstallationUpdateSchema(Schema):
    class Meta:
        ordered = True

    app_product = fields.String(
        required=False,
        metadata={"description": "Product name for the installation", "example": "GDM"},
    )

    app_version = fields.String(
        required=False,
        metadata={"description": "Version string of app", "example": "v19.1.31"},
    )


@openapi_schema(dhos_telemetry_api_spec)
class PatientInstallationRequest(SharedInstallationSchema):
    class Meta:
        title = "Patient Installation Request"
        unknown = EXCLUDE
        ordered = True

    date_first_launched = fields.String(
        required=True,
        metadata={
            "description": "ISO8601 datetime of first app launch",
            "example": "2020-01-01T00:00:00.000Z",
        },
    )

    phone_os = fields.String(
        required=True,
        metadata={"description": "Phone operating system", "example": "iOS"},
    )

    phone_os_version = fields.String(
        required=True,
        metadata={"description": "Phone operating system version", "example": "11.0"},
    )

    manufacturer = fields.String(
        required=True,
        metadata={"description": "Phone manufacturer", "example": "Apple, Inc."},
    )
    model = fields.String(
        required=True, metadata={"description": "Phone model", "example": "6"}
    )
    display_name = fields.String(
        required=True,
        metadata={"description": "Phone display name", "example": "Apple iPhone 6S"},
    )

    unique_device_code = fields.String(
        required=True,
        metadata={
            "description": "A unique code to identify the device",
            "example": "12345",
        },
    )


@openapi_schema(dhos_telemetry_api_spec)
class PatientInstallationResponse(PatientInstallationRequest, Identifier):
    class Meta:
        title = "Patient Installation Response"
        unknown = EXCLUDE
        ordered = True


@openapi_schema(dhos_telemetry_api_spec)
class PatientInstallationUpdateRequest(SharedInstallationUpdateSchema):
    class Meta:
        title = "Patient Installation Update Request"
        unknown = EXCLUDE
        ordered = True

    date_first_launched = fields.String(
        required=False,
        metadata={
            "description": "ISO8601 datetime of first app launch",
            "example": "2020-01-01T00:00:00.000Z",
        },
    )

    phone_os = fields.String(
        required=False,
        metadata={"description": "Phone operating system", "example": "iOS"},
    )

    phone_os_version = fields.String(
        required=False,
        metadata={"description": "Phone operating system version", "example": "11.0"},
    )

    manufacturer = fields.String(
        required=False,
        metadata={"description": "Phone manufacturer", "example": "Apple, Inc."},
    )

    model = fields.String(
        required=False, metadata={"description": "Phone model", "example": "6"}
    )

    display_name = fields.String(
        required=False,
        metadata={"description": "Phone display name", "example": "Apple iPhone 6S"},
    )


@openapi_schema(dhos_telemetry_api_spec)
class ClinicianInstallationRequest(SharedInstallationSchema):
    class Meta:
        title = "Clinician Installation Request"
        unknown = EXCLUDE
        ordered = True

    date_first_used = fields.String(
        required=True,
        metadata={
            "description": "ISO8601 datetime of first desktop use",
            "example": "2019-08-11T11:59:50.123+01:00",
        },
    )

    desktop_os = fields.String(
        required=True,
        metadata={"description": "Desktop operating system", "example": "Windows"},
    )

    desktop_os_version = fields.String(
        required=True,
        metadata={"description": "Desktop operating system version", "example": "10"},
    )

    ip_address = fields.String(
        required=True,
        metadata={"description": "IP Address of client", "example": "1.2.3.4"},
    )

    unique_device_code = fields.String(
        required=True,
        metadata={
            "description": "A unique code to identify the device",
            "example": "12345",
        },
    )


@openapi_schema(dhos_telemetry_api_spec)
class ClinicianInstallationResponse(ClinicianInstallationRequest, Identifier):
    class Meta:
        title = "Clinician Installation Response"
        unknown = EXCLUDE
        ordered = True


@openapi_schema(dhos_telemetry_api_spec)
class ClinicianInstallationUpdateRequest(SharedInstallationUpdateSchema):
    class Meta:
        title = "Clinician Installation Update Request"
        unknown = EXCLUDE
        ordered = True

    date_first_used = fields.String(
        required=False,
        metadata={
            "description": "ISO8601 datetime of first desktop use",
            "example": "2019-08-11T11:59:50.123+01:00",
        },
    )

    desktop_os = fields.String(
        required=False,
        metadata={"description": "Desktop operating system", "example": "Windows"},
    )

    desktop_os_version = fields.String(
        required=False,
        metadata={"description": "Desktop operating system version", "example": "10"},
    )

    ip_address = fields.String(
        required=False,
        metadata={"description": "IP Address of client", "example": "1.2.3.4"},
    )


@openapi_schema(dhos_telemetry_api_spec)
class BloodGlucoseMeterRequest(Schema):
    class Meta:
        title = "Bluetooth meter request"
        unknown = EXCLUDE
        ordered = True

    app_version = fields.String(
        required=False,
        metadata={"description": "Application version number", "example": "19.1.54"},
    )

    app_product = fields.String(
        required=False,
        metadata={"description": "Application product", "example": "GDM"},
    )

    date_verified = fields.AwareDateTime(
        required=False,
        metadata={
            "description": "ISO8601 datetime when verification of blood glucose reading was performed",
            "example": "2021-10-27T11:59:50.123+01:00",
        },
    )

    mobile_id = fields.String(
        required=True,
        metadata={
            "description": "Mobile device UUID",
            "example": "c28eb1cb-ca58-41b8-8acb-15721553f4f2",
        },
    )

    serial_number = fields.String(
        required=True,
        metadata={
            "description": "Bluetooth device serial number",
            "example": "SN987654321",
        },
    )

    is_bg_value_correct = fields.Boolean(
        required=False,
        metadata={
            "description": "Was the blood glucose reading correct",
            "example": True,
        },
    )

    blood_glucose_value = fields.Float(
        required=False,
        metadata={"description": "Blood glucose value", "example": "5.5"},
    )


@openapi_schema(dhos_telemetry_api_spec)
class BloodGlucoseMeterResponse(BloodGlucoseMeterRequest, Identifier):
    class Meta:
        title = "Bluetooth meter response"
        unknown = EXCLUDE
        ordered = True

    patient_id = fields.String(
        required=True,
        metadata={
            "description": "Associated patient's UUID",
            "example": "c28eb1cb-ca58-41b8-8acb-15721553f4f2",
        },
    )


@openapi_schema(dhos_telemetry_api_spec)
class BloodGlucoseMeterUpdate(Schema):
    class Meta:
        title = "Bluetooth meter update"
        unknown = EXCLUDE
        ordered = True

    patient_id = fields.String(
        required=False,
        metadata={
            "description": "Associated patient's UUID",
            "example": "c28eb1cb-ca58-41b8-8acb-15721553f4f2",
        },
    )

    app_product = fields.String(
        required=False,
        metadata={"description": "Application product", "example": "GDM"},
    )

    app_version = fields.String(
        required=False,
        metadata={"description": "Application version number", "example": "19.1.54"},
    )

    date_verified = fields.String(
        required=False,
        metadata={
            "description": "ISO8601 datetime when verification of blood glucose reading was performed",
            "example": "2021-10-27T11:59:50.123+01:00",
        },
    )

    mobile_id = fields.String(
        required=False,
        metadata={
            "description": "Mobile device UUID",
            "example": "c28eb1cb-ca58-41b8-8acb-15721553f4f2",
        },
    )

    serial_number = fields.String(
        required=False,
        metadata={
            "description": "Bluetooth device serial number",
            "example": "SN987654321",
        },
    )

    is_bg_value_correct = fields.Boolean(
        required=False,
        metadata={
            "description": "Was the blood glucose reading correct",
            "example": True,
        },
    )

    blood_glucose_value = fields.Float(
        required=False,
        metadata={"description": "Blood glucose value", "example": "5.5"},
    )
