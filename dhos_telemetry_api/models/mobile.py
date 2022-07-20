from datetime import datetime
from typing import Dict

from flask_batteries_included.helpers import timestamp
from flask_batteries_included.sqldb import ModelIdentifier, db


class Mobile(ModelIdentifier, db.Model):

    patient_id = db.Column(db.String(length=36), unique=False, nullable=False)
    unique_device_code = db.Column(db.String, unique=False, nullable=False)
    date_first_launched_ = db.Column(db.DateTime, unique=False, nullable=False)
    date_first_launched_time_zone_ = db.Column(db.Integer, unique=False, nullable=False)
    app_product = db.Column(db.String, unique=False, nullable=False)
    app_version = db.Column(db.String, unique=False, nullable=False)
    phone_os = db.Column(db.String, unique=False, nullable=False)
    phone_os_version = db.Column(db.String, unique=False, nullable=False)
    manufacturer = db.Column(db.String, unique=False, nullable=False)
    model = db.Column(db.String, unique=False, nullable=False)
    display_name = db.Column(db.String, unique=False, nullable=False)

    @property
    def date_first_launched(self) -> datetime:
        return timestamp.join_timestamp(
            self.date_first_launched_, self.date_first_launched_time_zone_
        )

    @date_first_launched.setter
    def date_first_launched(self, value: str) -> None:
        (
            self.date_first_launched_,
            self.date_first_launched_time_zone_,
        ) = timestamp.split_timestamp(value)

    @staticmethod
    def schema() -> Dict:
        return {
            "optional": {},
            "required": {
                "unique_device_code": str,
                "date_first_launched": str,
                "app_product": str,
                "app_version": str,
                "phone_os": str,
                "phone_os_version": str,
                "manufacturer": str,
                "model": str,
                "display_name": str,
            },
            "updatable": {
                "date_first_launched": str,
                "app_product": str,
                "app_version": str,
                "phone_os": str,
                "phone_os_version": str,
                "manufacturer": str,
                "model": str,
                "display_name": str,
            },
        }

    def to_dict(self) -> Dict:
        return {
            "patient_id": self.patient_id,
            "unique_device_code": self.unique_device_code,
            "date_first_launched": self.date_first_launched,
            "app_product": self.app_product,
            "app_version": self.app_version,
            "phone_os": self.phone_os,
            "phone_os_version": self.phone_os_version,
            "manufacturer": self.manufacturer,
            "model": self.model,
            "display_name": self.display_name,
            **self.pack_identifier(),
        }
