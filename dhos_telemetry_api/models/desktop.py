from datetime import datetime
from typing import Dict

from flask_batteries_included.helpers import timestamp
from flask_batteries_included.sqldb import ModelIdentifier, db


class Desktop(ModelIdentifier, db.Model):

    clinician_id = db.Column(db.String(length=36), unique=False, nullable=False)
    unique_device_code = db.Column(db.String, unique=False, nullable=False)
    date_first_used_ = db.Column(db.DateTime, unique=False, nullable=False)
    date_first_used_time_zone_ = db.Column(db.Integer, unique=False, nullable=False)
    app_product = db.Column(db.String, unique=False, nullable=False)
    app_version = db.Column(db.String, unique=False, nullable=False)
    desktop_os = db.Column(db.String, unique=False, nullable=False)
    desktop_os_version = db.Column(db.String, unique=False, nullable=False)
    ip_address = db.Column(db.String, unique=False, nullable=False)

    @property
    def date_first_used(self) -> datetime:
        return timestamp.join_timestamp(
            self.date_first_used_, self.date_first_used_time_zone_
        )

    @date_first_used.setter
    def date_first_used(self, value: str) -> None:
        (
            self.date_first_used_,
            self.date_first_used_time_zone_,
        ) = timestamp.split_timestamp(value)

    @staticmethod
    def schema() -> Dict:
        return {
            "optional": {},
            "required": {
                "unique_device_code": str,
                "date_first_used": str,
                "app_product": str,
                "app_version": str,
                "desktop_os": str,
                "desktop_os_version": str,
                "ip_address": str,
            },
            "updatable": {
                "date_first_used": str,
                "app_product": str,
                "app_version": str,
                "desktop_os": str,
                "desktop_os_version": str,
                "ip_address": str,
            },
        }

    def to_dict(self) -> Dict:
        return {
            "clinician_id": self.clinician_id,
            "unique_device_code": self.unique_device_code,
            "date_first_used": self.date_first_used,
            "app_product": self.app_product,
            "app_version": self.app_version,
            "desktop_os": self.desktop_os,
            "desktop_os_version": self.desktop_os_version,
            "ip_address": self.ip_address,
            **self.pack_identifier(),
        }
