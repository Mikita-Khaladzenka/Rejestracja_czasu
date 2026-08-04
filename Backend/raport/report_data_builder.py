from __future__ import annotations

from datetime import datetime, timedelta

from repositories.report_repository import ReportRepository
from raport.report_date_range import ReportDateRange


class ReportDataBuilder:
    """Buduje dane wykorzystywane do wygenerowania raportu."""

    _repository = ReportRepository()

    @classmethod
    def generate(
        cls,
        report_type: str,
        year: int | None = None,
        month: int | None = None,
        week: int | None = None,
    ) -> dict:

        start_date, end_date = ReportDateRange.get_date_range(
            report_type,
            year,
            month,
            week,
        )

        rows = cls._repository.get_report_data(
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d"),
        )

        dates = cls._build_dates(start_date, end_date)

        employees: dict = {}

        for row in rows:

            employee_id = row["pracownik_id"]

            if employee_id not in employees:
                employees[employee_id] = cls._create_employee(row, dates)

            cls._update_employee(employees[employee_id], row)

        return {
            "typ": report_type,
            "od": start_date,
            "do": end_date,
            "pracownicy": list(employees.values()),
        }

    @staticmethod
    def _build_dates(start_date, end_date):

        dates = []

        current = start_date

        while current <= end_date:
            dates.append(current)
            current += timedelta(days=1)

        return dates

    @classmethod
    def _create_employee(cls, row, dates):

        employee = {
            "imie": row["imie"],
            "nazwisko": row["nazwisko"],
            "process": row["process"],
            "dni": {},
            "suma": 0,
        }

        for current_date in dates:

            employee["dni"][current_date.strftime("%Y-%m-%d")] = {
                "R": "-",
                "K": "-",
                "nie_zakonczyl_prace": False,
            }

        return employee

    @classmethod
    def _update_employee(cls, employee: dict, row: dict):

        if not row["data"]:
            return

        employee["dni"][row["data"]] = {
            "R": cls.format_time(row["rozpoczecie"]),
            "K": cls.format_time(row["zakonczenie"]),
            "nie_zakonczyl_prace": row["nie_zakonczyl_prace"] == 1,
        }

        if row["czas_pracy"]:
            employee["suma"] += row["czas_pracy"]

    @staticmethod
    def format_time(value: str | None) -> str:

        if not value:
            return "-"

        try:
            return datetime.strptime(
                value,
                "%Y-%m-%d %H:%M:%S",
            ).strftime("%H:%M")

        except (ValueError, TypeError):
            return "-"