from datetime import datetime
from typing import Dict

from flask_batteries_included.helpers import timestamp
from flask_batteries_included.sqldb import ModelIdentifier, db
from sqlalchemy import UniqueConstraint


class BloodGlucoseMeter(ModelIdentifier, db.Model):
    __table_args__ = (
        UniqueConstraint(
            "patient_id",
            "serial_number",
            name="uix_blood_glucose_meter_patient_id_serial_number",
        ),
    )

    mobile_id = db.Column(db.String(length=36), unique=False, nullable=False)
    patient_id = db.Column(db.String(length=36), unique=False, nullable=False)
    serial_number = db.Column(db.String, unique=False, nullable=False)
    date_verified = db.Column(db.DateTime(timezone=True), unique=False, nullable=False)
    is_bg_value_correct = db.Column(db.Boolean, unique=False, nullable=True)
    app_product = db.Column(db.String, unique=False, nullable=False)
    app_version = db.Column(db.String, unique=False, nullable=False)
    blood_glucose_value = db.Column(db.Float, unique=False, nullable=False)

    @staticmethod
    def schema() -> Dict:
        return {
            "optional": {
                "date_verified": str,
                "is_bg_value_correct": bool,
                "app_product": str,
                "app_version": str,
                "blood_glucose_value": float,
            },
            "required": {
                "mobile_id": str,
                "serial_number": str,
            },
            "updatable": {
                "mobile_id": str,
                "serial_number": str,
                "date_verified": str,
                "is_bg_value_correct": bool,
                "app_version": str,
                "blood_glucose_value": float,
            },
        }

    def to_dict(self) -> Dict:
        return {
            "mobile_id": self.mobile_id,
            "patient_id": self.patient_id,
            "serial_number": self.serial_number,
            "date_verified": self.date_verified,
            "is_bg_value_correct": self.is_bg_value_correct,
            "app_product": self.app_product,
            "app_version": self.app_version,
            "blood_glucose_value": self.blood_glucose_value,
            **self.pack_identifier(),
        }
