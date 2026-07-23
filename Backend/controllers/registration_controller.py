from flask import Blueprint, request, jsonify

from services.registration_service import RegistrationService



registration_bp = Blueprint(
    "registration",
    __name__
)



@registration_bp.route(
    "/rejestracja",
    methods=["POST"]
)
def rejestracja():

    wynik = RegistrationService.register(
        request.get_json()
    )


    return jsonify(wynik)
