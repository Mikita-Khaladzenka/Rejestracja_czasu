from flask import Blueprint, request, jsonify

from services.registration_service import (
    RegistrationService
)


registration_bp = Blueprint(
    "registration",
    __name__
)


@registration_bp.route(
    "/rejestracja",
    methods=["POST"]
)
def rejestracja():

    data = request.get_json(
        silent=True
    ) or {}

    result = RegistrationService.register(
        data
    )

    return jsonify(result)
