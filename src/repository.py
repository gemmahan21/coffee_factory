from .database import Database

from src.dto import (
    MaterialDto,
    ProductDto,
    ProductionDto,
    ProductLotDto,
    ProductionMaterialDto,
)
from src.enum import ProductionStatus


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
        return self.db.fetch_all(query)


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

    def update_production_status(self, production_id: int, status: ProductionStatus):
        query = "update production set status = %s where production_id = %s;"
        self.db.execute(query, (status, production_id))

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

    def find_product_lot_no(self, lot_no: str):
        query = "select count(*) from product_lot where lot_no = %s::text;"

        count = self.db.get_row_count(query, (lot_no,))
        return count


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
        return self.db.fetch_all(query)
