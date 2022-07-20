from typing import Dict

from flask import Blueprint, Response, jsonify, make_response, request
from flask_batteries_included.helpers import schema
from flask_batteries_included.helpers.security import protected_route
from flask_batteries_included.helpers.security.endpoint_security import (
    and_,
    match_keys,
    or_,
    scopes_present,
)

from dhos_telemetry_api.blueprint_api import controller
from dhos_telemetry_api.models.blood_glucose_meter import BloodGlucoseMeter
from dhos_telemetry_api.models.desktop import Desktop
from dhos_telemetry_api.models.mobile import Mobile

api_blueprint = Blueprint("api", __name__)


@api_blueprint.route("/dhos/v1/patient/<patient_id>/installation", methods=["POST"])
@protected_route(
    and_(
        scopes_present(required_scopes="write:gdm_telemetry"),
        match_keys(patient_id="patient_id"),
    )
)
def create_patient_installation(patient_id: str) -> Response:
    """
    ---
    post:
      summary: Create patient installation
      description: Create a new patient installation using the details in the request body
      tags: [patient]
      parameters:
        - in: path
          name: patient_id
          required: true
          schema:
            type: string
            example: 5579f479-c28d-4657-b9e1-cdd36ca8ecad
      requestBody:
        required: true
        content:
          application/json:
            schema: PatientInstallationRequest
      responses:
        '200':
          description: New patient installation
          content:
            application/json:
              schema: PatientInstallationResponse
        default:
          description: >-
              Error, e.g. 400 Bad Request, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    _json = schema.post(**Mobile.schema())
    return jsonify(
        controller.create_mobile_installation(
            patient_id=patient_id, installation_data=_json
        )
    )


@api_blueprint.route(
    "/dhos/v1/patient/<patient_id>/installation/<installation_id>", methods=["PATCH"]
)
@protected_route(
    and_(
        scopes_present(required_scopes="write:gdm_telemetry"),
        match_keys(patient_id="patient_id"),
    )
)
def update_patient_installation(patient_id: str, installation_id: str) -> Response:
    """
    ---
    patch:
      summary: Update patient installation
      description: >-
        Update the patient installation with the provided UUID using the
        details provided in the request body
      tags: [patient]
      parameters:
        - in: path
          name: patient_id
          required: true
          schema:
            type: string
            example: 7b958ac5-0b8c-4c4e-b992-a87940b4439a
        - in: path
          name: installation_id
          required: true
          schema:
            type: string
            example: a25497b1-c9aa-42bd-bdda-896821073506
      requestBody:
        required: true
        content:
          application/json:
            schema: PatientInstallationUpdateRequest
      responses:
        200:
          description: Updated patient installation
          content:
            application/json:
              schema: PatientInstallationResponse
        default:
          description: >-
              Error, e.g. 400 Bad Request, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    if not request.is_json:
        raise TypeError("Request should contain a json body")

    _json = schema.update(**Mobile.schema())

    return jsonify(
        controller.update_installation(
            Mobile, _json, patient_id=patient_id, uuid=installation_id
        )
    )


@api_blueprint.route(
    "/dhos/v1/patient/<patient_id>/installation/<installation_id>", methods=["GET"]
)
@protected_route(
    or_(
        scopes_present(required_scopes="read:gdm_telemetry_all"),
        and_(
            scopes_present(required_scopes="read:gdm_telemetry"),
            match_keys(patient_id="patient_id"),
        ),
    )
)
def get_patient_installation(patient_id: str, installation_id: str) -> Response:
    """
    ---
    get:
      summary: Get patient installation by UUID
      description: Get the patient installation with the provided UUID
      tags: [patient]
      parameters:
        - in: path
          name: patient_id
          required: true
          schema:
            type: string
            example: 7b958ac5-0b8c-4c4e-b992-a87940b4439a
        - in: path
          name: installation_id
          required: true
          schema:
            type: string
            example: a25497b1-c9aa-42bd-bdda-896821073506
      responses:
        '200':
          description: The patient installation
          content:
            application/json:
              schema: PatientInstallationResponse
        default:
          description: >-
              Error, e.g. 400 Bad Request, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    if request.is_json:
        raise TypeError("Request should not contain a json body")

    schema.get()

    return jsonify(
        controller.retrieve_installation_by_id(
            Mobile, patient_id=patient_id, uuid=installation_id
        )
    )


@api_blueprint.route(
    "/dhos/v1/patient/<patient_id>/latest_installation", methods=["GET"]
)
@protected_route(
    or_(
        scopes_present(required_scopes="read:gdm_telemetry_all"),
        and_(
            scopes_present(required_scopes="read:gdm_telemetry"),
            match_keys(patient_id="patient_id"),
        ),
    )
)
def get_latest_patient_installation(patient_id: str) -> Response:
    """
    ---
    get:
      summary: Get latest patient installation
      description: Get the latest installation for the patient with the provided UUID
      tags: [patient]
      parameters:
        - in: path
          name: patient_id
          required: true
          schema:
            type: string
            example: 7b958ac5-0b8c-4c4e-b992-a87940b4439a
      responses:
        '200':
          description: Latest patient installation
          content:
            application/json:
              schema: PatientInstallationResponse
        default:
          description: >-
              Error, e.g. 400 Bad Request, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    if request.is_json:
        raise TypeError("Request should not contain a json body")

    schema.get()

    return jsonify(
        controller.retrieve_latest_installation(
            Mobile, order_by=Mobile.date_first_launched_, patient_id=patient_id
        )
    )


@api_blueprint.route("/dhos/v1/clinician/<clinician_id>/installation", methods=["POST"])
@protected_route(
    and_(
        scopes_present(required_scopes="write:gdm_telemetry"),
        match_keys(clinician_id="clinician_id"),
    )
)
def create_clinician_installation(clinician_id: str) -> Response:
    """
    ---
    post:
      summary: Create clinician installation
      description: Create a new clinician installation using the details in the request body
      tags: [clinician]
      parameters:
        - in: path
          name: clinician_id
          required: true
          schema:
            type: string
            example: 6ed98323-9302-4ad3-8c51-2e1ca938513e
      requestBody:
        required: true
        content:
          application/json:
            schema: ClinicianInstallationRequest
      responses:
        200:
          description: New clinician installation
          content:
            application/json:
              schema: ClinicianInstallationResponse
        default:
          description: >-
              Error, e.g. 400 Bad Request, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    _json = schema.post(**Desktop.schema())

    return jsonify(
        controller.create_desktop_installation(
            clinician_id=clinician_id, installation_data=_json
        )
    )


@api_blueprint.route(
    "/dhos/v1/clinician/<clinician_id>/installation/<installation_id>", methods=["GET"]
)
@protected_route(
    or_(
        scopes_present(required_scopes="read:gdm_telemetry_all"),
        and_(
            scopes_present(required_scopes="read:gdm_telemetry"),
            match_keys(clinician_id="clinician_id"),
        ),
    )
)
def get_clinician_installation(clinician_id: str, installation_id: str) -> Response:
    """
    ---
    get:
      summary: Get clinician installation by UUID
      description: Get the clinician installation with the provided UUID
      tags: [clinician]
      parameters:
        - in: path
          name: clinician_id
          required: true
          schema:
            type: string
            example: 7b958ac5-0b8c-4c4e-b992-a87940b4439a
        - in: path
          name: installation_id
          required: true
          schema:
            type: string
            example: a25497b1-c9aa-42bd-bdda-896821073506
      responses:
        '200':
          description: The clinician installation
          content:
            application/json:
              schema: ClinicianInstallationResponse
        default:
          description: >-
              Error, e.g. 400 Bad Request, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    if request.is_json:
        raise TypeError("Request should not contain a json body")

    schema.get()

    return jsonify(
        controller.retrieve_installation_by_id(
            Desktop, clinician_id=clinician_id, uuid=installation_id
        )
    )


@api_blueprint.route(
    "/dhos/v1/clinician/<clinician_id>/latest_installation", methods=["GET"]
)
@protected_route(
    or_(
        scopes_present(required_scopes="read:gdm_telemetry_all"),
        and_(
            scopes_present(required_scopes="read:gdm_telemetry"),
            match_keys(clinician_id="clinician_id"),
        ),
    )
)
def get_latest_clinician_installation(clinician_id: str) -> Response:
    """
    ---
    get:
      summary: Get latest clinician installation
      description: Get the latest installation for the clincian with the provided UUID
      tags: [clinician]
      parameters:
        - in: path
          name: clinician_id
          required: true
          schema:
            type: string
            example: 7b958ac5-0b8c-4c4e-b992-a87940b4439a
      responses:
        '200':
          description: Latest clinician installation
          content:
            application/json:
              schema: ClinicianInstallationResponse
        default:
          description: >-
              Error, e.g. 400 Bad Request, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    if request.is_json:
        raise TypeError("Request should not contain a json body")

    schema.get()

    return jsonify(
        controller.retrieve_latest_installation(
            Desktop,
            order_by=(Desktop.date_first_used_, Desktop.app_version),
            clinician_id=clinician_id,
        )
    )


@api_blueprint.route(
    "/dhos/v1/clinician/<clinician_id>/installation/<installation_id>",
    methods=["PATCH"],
)
@protected_route(
    and_(
        scopes_present(required_scopes="write:gdm_telemetry"),
        match_keys(clinician_id="clinician_id"),
    )
)
def update_clinician_installation(clinician_id: str, installation_id: str) -> Response:
    """
    ---
    patch:
      summary: Update clinician installation
      description: >-
        Update the clinician installation with the provided UUID using the
        details provided in the request body
      tags: [clinician]
      parameters:
        - in: path
          name: clinician_id
          required: true
          schema:
            type: string
            example: 7b958ac5-0b8c-4c4e-b992-a87940b4439a
        - in: path
          name: installation_id
          required: true
          schema:
            type: string
            example: a25497b1-c9aa-42bd-bdda-896821073506
      requestBody:
        required: true
        content:
          application/json:
            schema: ClinicianInstallationUpdateRequest
      responses:
        '200':
          description: Updated clinician installation
          content:
            application/json:
              schema: ClinicianInstallationResponse
        default:
          description: >-
              Error, e.g. 400 Bad Request, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    _json = schema.update(**Desktop.schema())

    return jsonify(
        controller.update_installation(
            Desktop, _json, clinician_id=clinician_id, uuid=installation_id
        )
    )


@api_blueprint.route(
    "/dhos/v1/patient/<patient_id>/blood_glucose_meter", methods=["POST"]
)
@protected_route(
    and_(
        scopes_present(required_scopes="write:gdm_telemetry"),
        match_keys(patient_id="patient_id"),
    )
)
def create_blood_glucose_meter(patient_id: str, meter_data: Dict) -> Response:
    """
    ---
    post:
      summary: Create patient blood glucose meter
      description: Create a patient blood glucose meter using the details in the request body
      tags: [blood-glucose-meter]
      parameters:
        - in: path
          name: patient_id
          required: true
          schema:
            type: string
            example: 5579f479-c28d-4657-b9e1-cdd36ca8ecad
      requestBody:
        required: true
        content:
          application/json:
            schema:
                x-body-name: meter_data
                $ref: '#/components/schemas/BloodGlucoseMeterRequest'
      responses:
        '201':
          description: New blood glucose meter
          content:
            application/json:
              schema: BloodGlucoseMeterResponse
        default:
          description: >-
              Error, e.g. 400 Bad Request, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    return make_response(
        jsonify(
            controller.create_blood_glucose_meter(
                patient_id=patient_id, meter_data=meter_data
            )
        ),
        201,
    )


@api_blueprint.route(
    "/dhos/v1/patient/<patient_id>/blood_glucose_meter/<meter_id>",
    methods=["PATCH"],
)
@protected_route(
    and_(
        scopes_present(required_scopes="write:gdm_telemetry"),
        match_keys(patient_id="patient_id"),
    )
)
def update_blood_glucose_meter(
    patient_id: str, meter_id: str, meter_data: Dict
) -> Response:
    """
    ---
    patch:
      summary: Update patient blood glucose meter
      description: Update a patient blood glucose meter using the details in the request body
      tags: [blood-glucose-meter]
      parameters:
        - in: path
          name: patient_id
          required: true
          schema:
            type: string
            example: 5579f479-c28d-4657-b9e1-cdd36ca8ecad
        - in: path
          name: meter_id
          required: true
          schema:
            type: string
            example: 85:65:78:65:78
      requestBody:
        required: true
        content:
          application/json:
            schema:
                x-body-name: meter_data
                $ref: '#/components/schemas/BloodGlucoseMeterUpdate'
      responses:
        '200':
          description: New blood glucose meter
          content:
            application/json:
              schema: BloodGlucoseMeterUpdate
        default:
          description: >-
              Error, e.g. 400 Bad Request, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    return jsonify(
        controller.update_blood_glucose_meter(
            meter_id=meter_id, patient_id=patient_id, update_data=meter_data
        )
    )


@api_blueprint.route(
    "/dhos/v1/patient/<patient_id>/blood_glucose_meter/<meter_id>", methods=["GET"]
)
@protected_route(
    and_(
        scopes_present(required_scopes="read:gdm_telemetry"),
        match_keys(patient_id="patient_id"),
    )
)
def get_blood_glucose_meter(patient_id: str, meter_id: str) -> Response:
    """
    ---
    get:
      summary: Get patient blood glucose meter
      description: Get a patient blood glucose meter by UUID
      tags: [blood-glucose-meter]
      parameters:
        - in: path
          name: meter_id
          required: true
          schema:
            type: string
            example: 85:65:78:65:78
        - in: path
          name: patient_id
          required: true
          schema:
            type: string
            example: 5579f479-c28d-4657-b9e1-cdd36ca8ecad
      responses:
        '200':
          description: Blood glucose meter
          content:
            application/json:
              schema: BloodGlucoseMeterResponse
        default:
          description: >-
              Error, e.g. 400 Bad Request, 503 Service Unavailable
          content:
            application/json:
              schema: Error
    """
    return jsonify(
        controller.get_blood_glucose_meter(patient_id=patient_id, meter_id=meter_id)
    )
