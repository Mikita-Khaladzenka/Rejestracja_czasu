from __future__ import annotations

from sqlite3 import Row

from database.database import Database


class ReportRepository:
    """Odpowiada za pobieranie danych raportów z bazy danych."""

    _REPORT_QUERY = """
        SELECT
            p.id AS pracownik_id,
            p.imie,
            p.nazwisko,
            p.process,
            c.data,
            c.rozpoczecie,
            c.zakonczenie,
            c.czas_pracy,
            c.nie_zakonczyl_prace
        FROM pracownicy p
        LEFT JOIN czas_pracy c
            ON p.id = c.pracownik_id
            AND c.data BETWEEN ? AND ?
        ORDER BY
            p.nazwisko,
            p.imie,
            c.data
    """

    def get_report_data(
        self,
        start_date: str,
        end_date: str,
    ) -> list[Row]:

        connection = Database.get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                self._REPORT_QUERY,
                (start_date, end_date),
            )

            return cursor.fetchall()

        finally:
            connection.close()