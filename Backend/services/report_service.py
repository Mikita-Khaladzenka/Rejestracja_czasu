from __future__ import annotations

from raport.report_date_range import ReportDateRange
from raport.report_filename import ReportFilename
from raport.report_data_builder import ReportDataBuilder
from raport.report_table_builder import ReportTableBuilder


class ReportService:
    """
    Fasada modułu raportów.

    Odpowiada za koordynację:
    dane -> tabela -> generator.
    """


    @staticmethod
    def get_date_range(
        report_type: str,
        year: int | None = None,
        month: int | None = None,
        week: int | None = None,
    ):

        return ReportDateRange.get_date_range(
            report_type,
            year,
            month,
            week,
        )


    @staticmethod
    def get_filename(
        report_type: str,
        file_format: str,
        year: int,
        month: int | None = None,
        week: int | None = None,
    ):

        return ReportFilename.get_filename(
            report_type=report_type,
            file_format=file_format,
            year=year,
            month=month,
            week=week,
        )


    @staticmethod
    def generate_report_data(
        report_type: str,
        year: int | None = None,
        month: int | None = None,
        week: int | None = None,
    ) -> dict:

        return ReportDataBuilder.generate(
            report_type,
            year,
            month,
            week,
        )


    @staticmethod
    def build_report_table(
        report_data: dict,
    ) -> dict:

        return ReportTableBuilder.build(
            report_data,
        )