from flask import (
    Blueprint,
    request,
    jsonify,
    session,
    send_from_directory,
    send_file
)

from io import BytesIO

from services.admin_service import AdminService
from services.report_service import ReportService

from raport.report_table_builder import ReportTableBuilder
from raport.excel_generator import ExcelGenerator
from raport.pdf_generator import PDFGenerator

from config import Config


admin_bp = Blueprint(
    "admin",
    __name__
)


@admin_bp.route("/adm")
def adm():

    return send_from_directory(
        Config.FRONTEND,
        "adm.html"
    )



@admin_bp.route(
    "/adm/login",
    methods=["POST"]
)
def adm_login():

    dane = request.get_json() or {}

    wynik = AdminService.login(
        dane
    )

    if wynik["success"]:
        session["admin"] = True

    return jsonify(wynik)



@admin_bp.route("/adm/pracownicy")
def adm_pracownicy():

    if not session.get("admin"):
        return jsonify([])

    lista = AdminService.get_workers()

    return jsonify(lista)



@admin_bp.route(
    "/adm/dodaj",
    methods=["POST"]
)
def adm_dodaj():

    if not session.get("admin"):

        return jsonify({
            "success": False
        })

    dane = request.get_json() or {}

    wynik = AdminService.add_worker(
        dane
    )

    return jsonify(wynik)


@admin_bp.route(
    "/adm/usun/<int:id>",
    methods=["DELETE"]
)
def adm_usun(id):

    if not session.get("admin"):

        return jsonify({
            "success": False,
            "komunikat": "Brak uprawnień."
        }), 401

    wynik = AdminService.delete_worker(
        id
    )

    return jsonify(wynik)


@admin_bp.route(
    "/adm/raport",
    methods=["POST"]
)
def adm_raport():

    if not session.get("admin"):
        return jsonify({
            "success": False
        }), 401

    dane = request.get_json() or {}

    report_type = dane.get("typ")
    file_format = dane.get("format")
    year = dane.get("year")
    month = dane.get("month")
    week = dane.get("week")

    if year:
        year = int(year)

    if month:
        month = int(month)

    if week:
        week = int(week)

    report_data = ReportService.generate_report_data(
        report_type,
        year=year,
        month=month,
        week=week
    )

    table_result = ReportTableBuilder.build(
        report_data
    )

    # ===============================
    # EXCEL
    # ===============================

    if file_format == "excel":

        workbook = ExcelGenerator.generate(
            table_result
        )

        output = BytesIO()

        workbook.save(
            output
        )

        output.seek(0)

        filename = ReportService.get_filename(
            report_type=report_type,
            file_format="xlsx",
            year=year,
            month=month,
            week=week,
        )

        return send_file(
            output,
            as_attachment=True,
            download_name=filename,
            mimetype=(
                "application/vnd.openxmlformats-"
                "officedocument.spreadsheetml.sheet"
            ),
        )

    # ===============================
    # PDF
    # ===============================

    if file_format == "pdf":

        pdf = PDFGenerator.generate(
            table_result
        )

        filename = ReportService.get_filename(
            report_type=report_type,
            file_format="pdf",
            year=year,
            month=month,
            week=week,
        )

        return send_file(
            pdf,
            as_attachment=True,
            download_name=filename,
            mimetype="application/pdf",
        )

    return jsonify({
        "success": False,
        "komunikat": "Nieznany format"
    }), 400