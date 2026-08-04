from __future__ import annotations

import calendar
from datetime import date, datetime, timedelta


class ReportDateRange:
    """Odpowiada za wyznaczanie zakresu dat raportu."""

    WEEKLY = "weekly"
    MONTHLY = "monthly"

    @classmethod
    def get_date_range(
        cls,
        report_type: str,
        year: int | None = None,
        month: int | None = None,
        week: int | None = None,
    ) -> tuple[date, date]:

        if report_type == cls.WEEKLY:
            return cls._weekly_range(year, week)

        if report_type == cls.MONTHLY:
            return cls._monthly_range(year, month)

        raise ValueError(f"Nieznany typ raportu: {report_type}")

    @staticmethod
    def _weekly_range(
        year: int | None,
        week: int | None,
    ) -> tuple[date, date]:

        today = datetime.now().date()

        if year and week:
            start = date.fromisocalendar(int(year), int(week), 1)
        else:
            start = today - timedelta(days=today.weekday())

        end = start + timedelta(days=6)

        return start, end

    @staticmethod
    def _monthly_range(
        year: int | None,
        month: int | None,
    ) -> tuple[date, date]:

        today = datetime.now().date()

        if year and month:
            start = date(int(year), int(month), 1)
        else:
            start = today.replace(day=1)

        last_day = calendar.monthrange(start.year, start.month)[1]

        end = start.replace(day=last_day)

        return start, end