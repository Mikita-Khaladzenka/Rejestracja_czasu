from flask import (
    Blueprint,
    request,
    jsonify,
    session,
    send_from_directory
)


from services.admin_service import AdminService

from config import Config



admin_bp = Blueprint(
    "admin",
    __name__
)



# ======================================
# STRONA ADMINA
# ======================================

@admin_bp.route("/adm")
def adm():


    return send_from_directory(

        Config.FRONTEND,

        "adm.html"

    )



# ======================================
# LOGOWANIE ADMINA
# ======================================

@admin_bp.route(
    "/adm/login",
    methods=["POST"]
)
def adm_login():


    dane = request.get_json()


    wynik = AdminService.login(
        dane
    )



    if wynik["success"]:

        session["admin"] = True



    return jsonify(
        wynik
    )



# ======================================
# LISTA PRACOWNIKÓW
# ======================================

@admin_bp.route(
    "/adm/pracownicy"
)
def adm_pracownicy():



    if not session.get("admin"):

        return jsonify([])



    lista = AdminService.get_workers()



    return jsonify(
        lista
    )



# ======================================
# DODAWANIE PRACOWNIKA
# ======================================

@admin_bp.route(
    "/adm/dodaj",
    methods=["POST"]
)
def adm_dodaj():



    if not session.get("admin"):


        return jsonify({

            "success":False

        })



    dane = request.get_json()



    wynik = AdminService.add_worker(
        dane
    )



    return jsonify(
        wynik
    )



# ======================================
# USUWANIE PRACOWNIKA
# ======================================

@admin_bp.route(
    "/adm/usun/<int:id>",
    methods=["DELETE"]
)
def adm_usun(id):



    if not session.get("admin"):


        return jsonify({

            "success":False

        })



    wynik = AdminService.delete_worker(
        id
    )



    return jsonify(
        wynik
    )
