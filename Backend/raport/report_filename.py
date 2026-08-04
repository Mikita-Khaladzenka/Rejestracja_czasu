from __future__ import annotations

from datetime import datetime


class ReportFilename:
    """Buduje nazwę pliku raportu."""

    WEEKLY = "weekly"
    MONTHLY = "monthly"

    MONTH_NAMES = {
        1: "styczeń",
        2: "luty",
        3: "marzec",
        4: "kwiecień",
        5: "maj",
        6: "czerwiec",
        7: "lipiec",
        8: "sierpień",
        9: "wrzesień",
        10: "październik",
        11: "listopad",
        12: "grudzień",
    }

    @classmethod
    def get_filename(
        cls,
        report_type: str,
        file_format: str,
        year: int,
        month: int | None = None,
        week: int | None = None,
        generated_date: datetime | None = None,
    ) -> str:
        generated_date = generated_date or datetime.now()

        if report_type == cls.WEEKLY:
            filename = cls._weekly_filename(
                year=year,
                week=week,
                generated_date=generated_date,
            )

        elif report_type == cls.MONTHLY:
            filename = cls._monthly_filename(
                year=year,
                month=month,
                generated_date=generated_date,
            )

        else:
            raise ValueError(
                f"Nieznany typ raportu: {report_type}"
            )

        extension = file_format.lower()

        return f"{filename}.{extension}"

    @staticmethod
    def _format_generated_date(
        generated_date: datetime,
    ) -> str:
        return generated_date.strftime("%d-%m-%Y")

    @classmethod
    def _weekly_filename(
        cls,
        year: int,
        week: int | None,
        generated_date: datetime,
    ) -> str:
        if week is None:
            raise ValueError(
                "Nie podano numeru tygodnia"
            )

        return (
            f"Raport za tydzień {week} {year} "
            f"wygenerowany "
            f"{cls._format_generated_date(generated_date)}"
        )

    @classmethod
    def _monthly_filename(
        cls,
        year: int,
        month: int | None,
        generated_date: datetime,
    ) -> str:
        if month is None:
            raise ValueError(
                "Nie podano numeru miesiąca"
            )

        if month not in cls.MONTH_NAMES:
            raise ValueError(
                f"Niepoprawny numer miesiąca: {month}"
            )

        month_name = cls.MONTH_NAMES[month]

        return (
            f"Raport za {month_name} {year} "
            f"wygenerowany "
            f"{cls._format_generated_date(generated_date)}"
        )