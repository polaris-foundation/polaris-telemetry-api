from typing import Dict, List

from behave import given, step
from behave.runner import Context
from clients.dhos_telemetry_client import (
    get_bg_meter,
    get_clinician_installation,
    get_latest_clinician_installation,
    get_latest_patient_installation,
    get_patient_installation,
    patch_clinician_installation,
    patch_patient_installation,
    post_bg_meter,
    post_clinician_installation,
    post_patient_installation,
)
from faker import Faker
from helpers.jwt_helper import get_clinician_token, get_patient_token
from helpers.request_helper import (
    generate_bg_meter_request,
    generate_clinician_installation_request,
    generate_patient_installation_request,
)
from requests import Response


@given("there exists a {clinician_or_patient}")
def get_installation_body(context: Context, clinician_or_patient: str) -> None:
    fake: Faker = Faker()
    context.current_id = fake.uuid4()
    if clinician_or_patient == "clinician":
        context.current_jwt = get_clinician_token(clinician_id=context.current_id)
    else:
        context.current_jwt = get_patient_token(patient_id=context.current_id)


@step("{clinician_or_patient_or_another}'s installation is stored")
def clinician_create_request(
    context: Context, clinician_or_patient_or_another: str
) -> None:
    if clinician_or_patient_or_another.endswith("clinician"):
        request_body: Dict = generate_clinician_installation_request()
        response: Response = post_clinician_installation(
            jwt=context.current_jwt,
            request_body=request_body,
            clinician_id=context.current_id,
        )
    elif clinician_or_patient_or_another.endswith("patient"):
        request_body = generate_patient_installation_request()
        response = post_patient_installation(
            jwt=context.current_jwt,
            request_body=request_body,
            patient_id=context.current_id,
        )
    else:
        raise ValueError(f"Unable to handle {clinician_or_patient_or_another}")

    assert response.status_code == 200
    response_json: Dict = response.json()
    assert "uuid" in response_json
    context.installation_uuid = response_json["uuid"]
    context.installation_response = response
    context.request_bodies.append(request_body)


@step(
    "another {clinician_or_patient_or_another}'s installation, but with greater application version is stored"
)
def clinician_create_with_greater_application_version_request(
    context: Context, clinician_or_patient_or_another: str
) -> None:
    request_body: Dict = context.request_bodies[-1]
    app_version_list: List = list(map(int, request_body["app_version"][1:].split(".")))
    app_version_list[-1] += 1
    request_body["app_version"] = f"v{'.'.join(str(v) for v in app_version_list)}"

    if clinician_or_patient_or_another.endswith("clinician"):
        response: Response = post_clinician_installation(
            jwt=context.current_jwt,
            request_body=request_body,
            clinician_id=context.current_id,
        )
    elif clinician_or_patient_or_another.endswith("patient"):
        response = post_patient_installation(
            jwt=context.current_jwt,
            request_body=request_body,
            patient_id=context.current_id,
        )
    else:
        raise ValueError(f"Unable to handle {clinician_or_patient_or_another}")

    assert response.status_code == 200
    response_json: Dict = response.json()
    assert "uuid" in response_json
    context.installation_uuid = response_json["uuid"]
    context.installation_response = response
    context.request_bodies.append(request_body)


@step("the {latest_or_installation} details are returned")
def assert_clinician_installation_returned(
    context: Context, latest_or_installation: str
) -> None:
    if latest_or_installation == "latest installation":
        # latest = _first used_ most recently, not the one _submitted_ most recently
        expected: Dict = sorted(
            context.request_bodies,
            key=lambda x: (
                x.get("date_first_used", x.get("date_first_launched")),
                x["app_version"],
            ),
        )[-1]
    else:
        expected = context.request_bodies[-1]

    response_json: Dict = context.installation_response.json()
    for field in expected:
        assert (
            expected[field] == response_json[field]
        ), f"Expected {expected[field]}, got {response_json[field]} for field {field}"


@step("the {clinician_or_patient}'s installation is retrieved by its uuid")
def get_installation_by_uuid(context: Context, clinician_or_patient: str) -> None:
    if clinician_or_patient == "clinician":
        context.installation_response = get_clinician_installation(
            jwt=context.current_jwt,
            clinician_id=context.current_id,
            installation_id=context.installation_uuid,
        )
    else:
        context.installation_response = get_patient_installation(
            jwt=context.current_jwt,
            patient_id=context.current_id,
            installation_id=context.installation_uuid,
        )


@step("{clinician_or_patient}'s latest installation is retrieved")
def get_clinicians_latest_installation(
    context: Context, clinician_or_patient: str
) -> None:
    if clinician_or_patient == "clinician":
        context.installation_response = get_latest_clinician_installation(
            jwt=context.current_jwt,
            clinician_id=context.current_id,
        )
    else:
        context.installation_response = get_latest_patient_installation(
            jwt=context.current_jwt,
            patient_id=context.current_id,
        )


@step("the {clinician_or_patient}'s installation is updated")
def clinician_update_request(context: Context, clinician_or_patient: str) -> None:
    request_body: Dict = (
        generate_clinician_installation_request()
        if clinician_or_patient == "clinician"
        else generate_patient_installation_request()
    )
    # unique_device_code can't be updated
    del request_body["unique_device_code"]

    if clinician_or_patient == "clinician":
        response: Response = patch_clinician_installation(
            jwt=context.current_jwt,
            request_body=request_body,
            clinician_id=context.current_id,
            installation_id=context.installation_uuid,
        )
    else:
        response = patch_patient_installation(
            jwt=context.current_jwt,
            request_body=request_body,
            patient_id=context.current_id,
            installation_id=context.installation_uuid,
        )

    assert response.status_code == 200
    context.installation_response = response
    context.request_bodies.append(request_body)


@step("the meter is stored")
def meter_create_request(context: Context) -> None:

    request_body: Dict = generate_bg_meter_request()
    response: Response = post_bg_meter(
        jwt=context.current_jwt,
        request_body=request_body,
        patient_id=context.current_id,
    )

    assert response.status_code == 201
    response_json: Dict = response.json()
    assert "uuid" in response_json
    context.mobile_id = response_json["uuid"]
    context.meter_response = response
    context.meter_request = request_body


@step("the blood glucose meter is returned")
def assert_meter_details_returned(context: Context) -> None:
    response_json: Dict = context.meter_response.json()
    for field in context.meter_request:
        assert (
            context.meter_request[field] == response_json[field]
        ), f"Expected {context.meter_request[field]}, got {response_json[field]} for field {field}"


@step("the blood glucose meter is requested by its uuid")
def get_meter_by_uuid(context: Context) -> None:

    context.meter_response = get_bg_meter(
        jwt=context.current_jwt,
        meter_id=context.mobile_id,
        patient_id=context.current_id,
    )
