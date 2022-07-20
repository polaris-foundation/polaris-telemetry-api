from typing import Dict

import requests
from environs import Env
from requests import Response


def _get_base_url() -> str:
    return Env().str("DHOS_TELEMETRY_BASE_URL", "http://dhos-telemetry-api:5000")


def post_clinician_installation(
    request_body: Dict, clinician_id: str, jwt: str
) -> Response:
    return requests.post(
        url=f"{_get_base_url()}/dhos/v1/clinician/{clinician_id}/installation",
        timeout=15,
        headers={"Authorization": f"Bearer {jwt}"},
        json=request_body,
    )


def get_clinician_installation(
    clinician_id: str, installation_id: str, jwt: str
) -> Response:
    return requests.get(
        url=f"{_get_base_url()}/dhos/v1/clinician/{clinician_id}/installation/{installation_id}",
        timeout=15,
        headers={"Authorization": f"Bearer {jwt}"},
    )


def get_latest_clinician_installation(clinician_id: str, jwt: str) -> Response:
    return requests.get(
        url=f"{_get_base_url()}/dhos/v1/clinician/{clinician_id}/latest_installation",
        timeout=15,
        headers={"Authorization": f"Bearer {jwt}"},
    )


def patch_clinician_installation(
    clinician_id: str, installation_id: str, request_body: Dict, jwt: str
) -> Response:
    return requests.patch(
        url=f"{_get_base_url()}/dhos/v1/clinician/{clinician_id}/installation/{installation_id}",
        timeout=15,
        headers={"Authorization": f"Bearer {jwt}"},
        json=request_body,
    )


def post_patient_installation(
    request_body: Dict, patient_id: str, jwt: str
) -> Response:
    return requests.post(
        url=f"{_get_base_url()}/dhos/v1/patient/{patient_id}/installation",
        timeout=15,
        headers={"Authorization": f"Bearer {jwt}"},
        json=request_body,
    )


def get_patient_installation(
    patient_id: str, installation_id: str, jwt: str
) -> Response:
    return requests.get(
        url=f"{_get_base_url()}/dhos/v1/patient/{patient_id}/installation/{installation_id}",
        timeout=15,
        headers={"Authorization": f"Bearer {jwt}"},
    )


def get_latest_patient_installation(patient_id: str, jwt: str) -> Response:
    return requests.get(
        url=f"{_get_base_url()}/dhos/v1/patient/{patient_id}/latest_installation",
        timeout=15,
        headers={"Authorization": f"Bearer {jwt}"},
    )


def patch_patient_installation(
    patient_id: str, installation_id: str, request_body: Dict, jwt: str
) -> Response:
    return requests.patch(
        url=f"{_get_base_url()}/dhos/v1/patient/{patient_id}/installation/{installation_id}",
        timeout=15,
        headers={"Authorization": f"Bearer {jwt}"},
        json=request_body,
    )


def post_bg_meter(request_body: Dict, patient_id: str, jwt: str) -> Response:
    return requests.post(
        url=f"{_get_base_url()}/dhos/v1/patient/{patient_id}/blood_glucose_meter",
        timeout=15,
        headers={"Authorization": f"Bearer {jwt}"},
        json=request_body,
    )


def get_bg_meter(meter_id: str, patient_id: str, jwt: str) -> Response:
    return requests.get(
        url=f"{_get_base_url()}/dhos/v1/patient/{patient_id}/blood_glucose_meter/{meter_id}",
        timeout=15,
        headers={"Authorization": f"Bearer {jwt}"},
    )
