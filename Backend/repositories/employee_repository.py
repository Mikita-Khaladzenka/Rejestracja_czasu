from database.database import Database
from models.employee import Employee


class EmployeeRepository:

    def find_by_id(
        self,
        id,
    ):
        conn = Database.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM pracownicy
                WHERE id = ?
                """,
                (id,),
            )

            row = cursor.fetchone()

        finally:
            conn.close()

        if not row:
            return None

        return Employee(
            row["id"],
            row["imie"],
            row["nazwisko"],
            row["process"],
        )

    def find_all(self):
        conn = Database.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM pracownicy
                ORDER BY id
                """
            )

            rows = cursor.fetchall()

        finally:
            conn.close()

        return [
            Employee(
                row["id"],
                row["imie"],
                row["nazwisko"],
                row["process"],
            )
            for row in rows
        ]

    def save(
        self,
        employee,
    ):
        conn = Database.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO pracownicy (
                    id,
                    imie,
                    nazwisko,
                    process
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    employee.id,
                    employee.imie,
                    employee.nazwisko,
                    employee.process,
                ),
            )

            conn.commit()

        finally:
            conn.close()

    def delete(
        self,
        id,
    ):
        conn = Database.get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                DELETE FROM pracownicy
                WHERE id = ?
                """,
                (id,),
            )

            conn.commit()

            return cursor.rowcount > 0

        finally:
            conn.close()