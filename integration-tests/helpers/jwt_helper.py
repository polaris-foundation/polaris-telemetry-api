from typing import Optional

from environs import Env
from faker import Faker
from jose import jwt as jose_jwt


def get_clinician_token(clinician_id: str = None) -> str:
    return _get_token(subject="clinician", id=clinician_id)


def get_patient_token(patient_id: str = None) -> str:
    return _get_token(subject="patient", id=patient_id)


def _get_token(subject: str = None, id: str = None) -> str:
    fake: Faker = Faker()
    env: Env = Env()
    hs_issuer: str = env.str("HS_ISSUER")
    hs_key: str = env.str("HS_KEY")
    proxy_url: str = env.str("PROXY_URL")

    return jose_jwt.encode(
        {
            "metadata": {f"{subject}_id": id},
            "iss": hs_issuer,
            "aud": proxy_url + "/",
            "scope": "read:gdm_telemetry write:gdm_telemetry read:gdm_telemetry_all ",
            "exp": 9_999_999_999,
        },
        key=hs_key,
        algorithm="HS512",
    )
