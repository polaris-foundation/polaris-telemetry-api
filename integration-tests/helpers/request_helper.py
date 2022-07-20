from typing import Dict
from uuid import uuid4

from faker import Faker


def generate_clinician_installation_request() -> Dict:
    fake = Faker()
    return {
        "app_product": "GDM",
        "app_version": fake.pystr_format(
            string_format="v{{random_int}}.{{random_int}}.{{random_int}}"
        ),
        "date_first_used": fake.date(pattern="%Y-%m-%dT%H:%M:%S.000Z"),
        "desktop_os": "Windows",
        "desktop_os_version": "10",
        "ip_address": fake.ipv4(),
        "unique_device_code": str(fake.random_number(digits=6, fix_len=True)),
    }


def generate_patient_installation_request() -> Dict:
    fake = Faker()
    return {
        "app_product": "GDM",
        "app_version": fake.pystr_format(
            string_format="v{{random_int}}.{{random_int}}.{{random_int}}"
        ),
        "date_first_launched": fake.date(pattern="%Y-%m-%dT%H:%M:%S.000Z"),
        "display_name": "Apple iPhone 6S",
        "manufacturer": "Apple, Inc.",
        "model": "6",
        "phone_os": "iOS",
        "phone_os_version": "11.0",
        "unique_device_code": str(fake.random_number(digits=6, fix_len=True)),
    }


def generate_bg_meter_request() -> Dict:
    fake = Faker()
    return {
        "app_product": "GDM",
        "app_version": fake.pystr_format(
            string_format="v{{random_int}}.{{random_int}}.{{random_int}}"
        ),
        "date_verified": fake.date(pattern="%Y-%m-%dT%H:%M:%S.000Z"),
        "is_bg_value_correct": True,
        "serial_number": str(fake.random_number(digits=6, fix_len=True)),
        "mobile_id": str(uuid4()),
        "blood_glucose_value": 11.0,
    }
