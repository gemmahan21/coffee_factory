import psycopg
from psycopg.rows import dict_row
import os

from .models import Product, Production, Material


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

            id = cursor.lastrowid
            print(f"insert row id : {id}")

            conn.commit()
            cursor.close()

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
        except psycopg.DataError as e:
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

        except psycopg.DataError as e:
            print(f"{e}")
            return None

    def __enter__(self):
        self.connect()
        return self

    def close(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None

    def __exit__(self, exc_type, exc, tb):
        self.close()


class ProductRepository:
    def __init__(self, db: Database):
        self.db = db

    def add_product(self, product: Product):
        query = """
            insert into product (product_code, product_name, product_type, is_active)
            values (%s, %s, %s, %s);
        """
        params = {
            "product_code": product.product_code,
            "product_name": product.product_name,
            "product_type": product.product_type,
            "is_active": product.is_active,
        }

        self.db.execute(query, params)

    def find_all(self):
        query = "select * from product;"
        self.db.fetch_all(query)


class ProductionRepository:
    def __init__(self, db: Database):
        self.db = db

    def create_production(self, production: Production):
        query = """
            insert into production (product_code, product_id, quantity, unit, status)
            values (%s, %s, %s, %s, %s);
        """
        params = {
            "production_code": production.production_code,
            "product_id": production.product_id,
            "quantity": production.quantity,
            "unit": production.unit,
            "status": production.unit,
        }

        self.db.execute(query, params)


class MaterialRepository:
    def __init__(self, db: Database):
        self.db = db

    def add_material(self, material: Material):
        query = """
            insert into material (material_code, material_name, category)
            values (%s, %s, %s);
        """
        params = {
            "material_code": material.material_code,
            "material_name": material.material_name,
            "category": material.category,
        }

        self.db.execute(query, params)

    def find_all(self):
        query = "select * from material;"
        self.db.fetch_all(query)
