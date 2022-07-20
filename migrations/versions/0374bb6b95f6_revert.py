"""meter

Revision ID: 0374bb6b95f6
Revises: 22b454c57440
Create Date: 2021-11-22 16:23:20.855184

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0374bb6b95f6"
down_revision = "22b454c57440"
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint(
        "uix_blood_glucose_meter_patient_id_serial_number",
        "blood_glucose_meter",
        type_="unique",
    )


def downgrade():
    op.create_unique_constraint(
        "uix_blood_glucose_meter_patient_id_serial_number",
        "blood_glucose_meter",
        ["patient_id", "serial_number"],
    )
