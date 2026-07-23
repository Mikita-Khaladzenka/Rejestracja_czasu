from database.database import Database



class WorkTimeRepository:



    def get_last_by_employee(
        self,
        employee_id
    ):


        conn = Database.get_connection()

        cur = conn.cursor()


        cur.execute(
            """
            SELECT *
            FROM czas_pracy
            WHERE pracownik_id=?
            ORDER BY id DESC
            LIMIT 1
            """,
            (employee_id,)
        )


        row = cur.fetchone()


        conn.close()


        return row



    def close_work(
        self,
        id,
        end_time,
        seconds
    ):


        conn = Database.get_connection()

        cur = conn.cursor()


        cur.execute(
            """
            UPDATE czas_pracy
            SET zakonczenie=?,
                czas_pracy=?,
                nie_zakonczyl_prace=0
            WHERE id=?
            """,
            (
                end_time,
                seconds,
                id
            )
        )


        conn.commit()

        conn.close()



    def mark_not_finished(
        self,
        id
    ):


        conn = Database.get_connection()

        cur = conn.cursor()


        cur.execute(
            """
            UPDATE czas_pracy
            SET nie_zakonczyl_prace=1
            WHERE id=?
            """,
            (id,)
        )


        conn.commit()

        conn.close()



    def create(
        self,
        employee_id,
        date,
        start
    ):


        conn = Database.get_connection()

        cur = conn.cursor()


        cur.execute(
            """
            INSERT INTO czas_pracy
            (
                pracownik_id,
                data,
                rozpoczecie,
                nie_zakonczyl_prace
            )
            VALUES (?,?,?,0)
            """,
            (
                employee_id,
                date,
                start
            )
        )


        conn.commit()

        conn.close()
