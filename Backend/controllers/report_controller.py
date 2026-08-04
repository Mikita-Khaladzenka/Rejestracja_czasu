from flask import (
    Blueprint,
    request,
    send_file,
    jsonify,
)

from services.report_service import ReportService
from raport.pdf_generator import PDFGenerator
from raport.excel_generator import ExcelGenerator


report_bp = Blueprint(
    "report",
    __name__,
)


class ReportController:

    FORMATS = {
        "pdf",
        "xlsx",
    }

    TYPES = {
        "weekly",
        "monthly",
    }


    @staticmethod
    @report_bp.route(
        "/report/generate",
        methods=["GET"],
    )
    def generate_report():

        try:

            params = ReportController._get_parameters()

            ReportController._validate(
                params
            )


            data = ReportService.generate_report_data(
                params["type"],
                params["year"],
                params["month"],
                params["week"],
            )


            table = ReportService.build_report_table(
                data
            )


            file = ReportController._generate_file(
                params["format"],
                table,
            )


            filename = ReportService.get_filename(
                params["type"],
                params["format"],
            )


            return send_file(
                file,
                as_attachment=True,
                download_name=filename,
            )


        except ValueError as error:

            return jsonify(
                {
                    "error": str(error)
                }
            ), 400



    @staticmethod
    def _get_parameters():

        return {

            "type":
                request.args.get("type"),


            "format":
                request.args.get(
                    "format",
                    "pdf"
                ).lower(),


            "year":
                request.args.get("year"),


            "month":
                request.args.get("month"),


            "week":
                request.args.get("week"),

        }



    @classmethod
    def _validate(
        cls,
        params,
    ):

        if params["type"] not in cls.TYPES:

            raise ValueError(
                "Niepoprawny typ raportu"
            )


        if params["format"] not in cls.FORMATS:

            raise ValueError(
                "Niepoprawny format"
            )



    @staticmethod
    def _generate_file(
        file_format,
        table,
    ):

        if file_format == "pdf":

            return PDFGenerator.generate(
                table
            )


        if file_format == "xlsx":

            return ExcelGenerator.generate(
                table
            )


        raise ValueError(
            "Nieobsługiwany format"
        )