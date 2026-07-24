import psycopg
from psycopg.rows import dict_row
import os


class Database:
    def __init__(self):
        self.conn = None

    def connect(self):
        try:
            if self.conn is None:
                self.conn = psycopg.connect(
                    host=os.getenv("DB_HOST"),
                    port=os.getenv("DB_PORT"),
                    dbname=os.getenv("DB_NAME"),
                    user=os.getenv("DB_USER"),
                    password=os.getenv("DB_PASSWORD"),
                    row_factory=dict_row,
                )
            return self.conn

        except psycopg.errors.ConnectionTimeout as e:
            raise RuntimeError(f"DB connect Error : {e}")

    def execute(self, query, params=()):
        conn = self.connect()

        try:
            cursor = conn.cursor()

            cursor.execute(query, params)
            row = cursor.fetchone()

            conn.commit()
            cursor.close()

            if row is None:
                return None

            return dict(row)

        except psycopg.OperationalError as e:
            conn.rollback()
            print(f"Execute Error : {e}")

    def fetch_all(self, query, params=()):
        conn = self.connect()

        try:
            cursor = conn.cursor()

            cursor.execute(query, params)
            rows = cursor.fetchall()

            result = []
            for row in rows:
                result.append(dict(row))

            cursor.close()

            return result
        except psycopg.Error as e:
            print(f"{e}")
            return []

    def fetch_one(self, query, params=()):
        conn = self.connect()

        try:
            cursor = conn.cursor()

            cursor.execute(query, params)
            row = cursor.fetchone()

            if row is None:
                return None

            cursor.close()

            return dict(row)

        except psycopg.Error as e:
            print(f"{e}")
            return None

    def get_row_count(self, query, params=()):
        conn = self.connect()

        try:
            cursor = conn.cursor()

            cursor.execute(query, params)
            row = cursor.fetchone()

            if row is None:
                return 0

            return row.get("count")

        except psycopg.Error as e:
            print(f"{e}")
            return 0

    def execute_delete(self, query, params=()):
        conn = self.connect()

        try:
            cursor = conn.cursor()

            cursor.execute(query, params)

            conn.commit()
            cursor.close()

        except psycopg.OperationalError as e:
            conn.rollback()
            print(f"Execute Error : {e}")

    def __enter__(self):
        self.connect()
        return self

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def __exit__(self, exc_type, exc, tb):
        self.close()
