from __future__ import annotations

from datetime import date, timedelta


class ReportTableBuilder:
    """Buduje strukturę tabeli wykorzystywaną przez generatory raportów."""

    HEADER_NAME = "Imię"
    HEADER_SURNAME = "Nazwisko"
    HEADER_TOTAL = "Suma"

    START_COLUMN = "R"
    END_COLUMN = "K"

    @classmethod
    def build(cls, report_data: dict) -> dict:
        dates = cls._build_dates(
            report_data["od"],
            report_data["do"],
        )

        table = [
            cls._build_header(dates),
            cls._build_subheader(dates),
        ]

        merged = cls._build_merge_ranges(dates)
        red_cells: list[tuple[int, int]] = []

        cls._build_employee_rows(
            table=table,
            red_cells=red_cells,
            employees=report_data["pracownicy"],
            dates=dates,
        )

        return {
            "table": table,
            "merged": merged,
            "red_cells": red_cells,
        }

    @staticmethod
    def _build_dates(
        start: date,
        end: date,
    ) -> list[date]:
        dates = []
        current = start

        while current <= end:
            dates.append(current)
            current += timedelta(days=1)

        return dates

    @classmethod
    def _build_header(
        cls,
        dates: list[date],
    ) -> list[str]:

        header = [
            cls.HEADER_NAME,
            cls.HEADER_SURNAME,
        ]

        for current_date in dates:
            header.append(current_date.strftime("%d.%m.%Y"))
            header.append("")

        header.append(cls.HEADER_TOTAL)

        return header

    @classmethod
    def _build_subheader(
        cls,
        dates: list[date],
    ) -> list[str]:

        header = ["", ""]

        for _ in dates:
            header.extend(
                [
                    cls.START_COLUMN,
                    cls.END_COLUMN,
                ]
            )

        header.append("")

        return header

    @staticmethod
    def _build_merge_ranges(
        dates: list[date],
    ) -> list[tuple[int, int, int, int]]:

        merged = [
            (1, 1, 1, 2),
            (2, 1, 2, 2),
        ]

        column = 3

        for _ in dates:
            merged.append(
                (
                    column,
                    1,
                    column + 1,
                    1,
                )
            )
            column += 2

        merged.append(
            (
                column,
                1,
                column,
                2,
            )
        )

        return merged

    @classmethod
    def _build_employee_rows(
        cls,
        table: list,
        red_cells: list,
        employees: list,
        dates: list[date],
    ) -> None:

        row_index = 2

        for employee in employees:

            row_index += 1

            row = cls._build_employee_row(
                employee,
                dates,
                row_index,
                red_cells,
            )

            table.append(row)

    @classmethod
    def _build_employee_row(
        cls,
        employee: dict,
        dates: list[date],
        row_index: int,
        red_cells: list,
    ) -> list:

        row = [
            employee["imie"],
            employee["nazwisko"],
        ]

        for current_date in dates:

            day = employee["dni"][
                current_date.strftime("%Y-%m-%d")
            ]

            row.append(day["R"])
            row.append(day["K"])

            if day["nie_zakonczyl_prace"]:
                red_cells.append(
                    (
                        row_index,
                        len(row),
                    )
                )

        row.append(
            cls.seconds_to_time(
                employee["suma"]
            )
        )

        return row

    @staticmethod
    def seconds_to_time(
        seconds: int | None,
    ) -> str:

        if not seconds:
            return "00:00"

        hours = seconds // 3600
        minutes = (seconds % 3600) // 60

        return f"{hours:02}:{minutes:02}"