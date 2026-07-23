import sqlite3

from config import Config


class Database:


    @staticmethod
    def get_connection():

        conn = sqlite3.connect(
            Config.DB,
            timeout=10
        )

        conn.row_factory = sqlite3.Row


        conn.execute(
            """
            PRAGMA journal_mode=WAL;
            """
        )


        return conn
