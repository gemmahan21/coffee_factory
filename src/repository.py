from .database import Database

from src.dto import (
    MaterialDto,
    ProductDto,
    ProductionDto,
    ProductLotDto,
    ProductionMaterialDto,
)
from src.models import Material


class ProductRepository:
    def __init__(self, db: Database):
        self.db = db

    def add_product(self, product: ProductDto):
        query = """
            insert into product (product_code, product_name, product_type, is_active)
            values (%s, %s, %s, %s);
        """
        params = (
            product.product_code,
            product.product_name,
            product.product_type,
            product.is_active,
        )

        self.db.execute(query, params)

    def find_all(self):
        query = "select * from product;"
        self.db.fetch_all(query)


class ProductionRepository:
    def __init__(self, db: Database):
        self.db = db

    def add_production(self, production: ProductionDto):
        query = """
            insert into production (product_code, product_id, quantity, unit, status)
            values (%s, %s, %s, %s, %s);
        """
        params = (
            production.production_code,
            production.product_id,
            production.quantity,
            production.unit,
            production.status,
        )

        self.db.execute(query, params)

    def add_proudct_lot(self, lot: ProductLotDto):
        query = """
            insert into product_lot (lot_no, product_id)
            values (%s, %s);
        """
        params = (lot.lot_no, lot.production_id)
        self.db.execute(query, params)

    def add_production_material(self, productionMaterial: ProductionMaterialDto):
        query = """
            insert into production_material (production_id, material_id, quantity, unit)
            values (%s, %s);
        """
        params = (
            productionMaterial.production_id,
            productionMaterial.material_id,
            productionMaterial.quantity,
            productionMaterial.unit,
        )
        self.db.execute(query, params)


class MaterialRepository:
    def __init__(self, db: Database):
        self.db = db

    def add_material(self, material: MaterialDto):
        query = """
            insert into material (material_code, material_name, category)
            values (%s, %s, %s);
        """

        # print(material.__dict__)
        params = (material.material_code, material.material_name, material.category)

        self.db.execute(query, params)

    def find_all(self):
        query = "select * from material;"
        self.db.fetch_all(query)
