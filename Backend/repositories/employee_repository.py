from database.database import Database
from models.employee import Employee



class EmployeeRepository:


    def find_by_id(
        self,
        id
    ):


        conn = Database.get_connection()

        cur = conn.cursor()


        cur.execute(
            """
            SELECT *
            FROM pracownicy
            WHERE id=?
            """,
            (id,)
        )


        row = cur.fetchone()


        conn.close()



        if not row:

            return None



        return Employee(

            row["id"],

            row["imie"],

            row["process"]

        )



    def find_all(self):


        conn = Database.get_connection()

        cur = conn.cursor()


        cur.execute(
            """
            SELECT *
            FROM pracownicy
            ORDER BY id
            """
        )


        rows = cur.fetchall()


        conn.close()



        return [

            Employee(

                x["id"],

                x["imie"],

                x["process"]

            )

            for x in rows

        ]



    def save(
        self,
        employee
    ):


        conn = Database.get_connection()

        cur = conn.cursor()


        cur.execute(
            """
            INSERT INTO pracownicy
            (
                id,
                imie,
                process
            )
            VALUES (?,?,?)
            """,
            (
                employee.id,
                employee.imie,
                employee.process
            )
        )


        conn.commit()

        conn.close()



    def delete(
        self,
        id
    ):


        conn = Database.get_connection()

        cur = conn.cursor()


        cur.execute(
            """
            DELETE FROM pracownicy
            WHERE id=?
            """,
            (id,)
        )


        conn.commit()

        conn.close()
