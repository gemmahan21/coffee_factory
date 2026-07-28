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
            values (%s, %s, %s, %s)
            returning product_id;
        """
        params = (
            product.product_code,
            product.product_name,
            product.product_type,
            product.is_active,
        )

        return self.db.execute(query, params)

    def update_product_status(self, is_active: bool, product_id: int):
        query = "update product set is_active = %s where product_id = %s returning product_id, is_active;"

        return self.db.execute(query, (is_active, product_id))

    def find_all(self):
        query = "select * from product order by product_id;"
        return self.db.fetch_all(query)


class MaterialRepository:
    def __init__(self, db: Database):
        self.db = db

    def add_material(self, material: MaterialDto):
        query = """
            insert into material (material_code, material_name, category)
            values (%s, %s, %s)
            returning material_id;
        """

        # print(material.__dict__)
        params = (material.material_code, material.material_name, material.category)

        return self.db.execute(query, params)

    def find_all(self):
        query = "select * from material order by material_id;"
        return self.db.fetch_all(query)

    def remove_material(self, material_id: int):
        query = "delete from production_material where material_id = %s;"
        self.db.execute_delete(query, (material_id,))

        query = "delete from material where material_id = %s;"
        self.db.execute_delete(query, (material_id,))


class ProductionRepository:
    def __init__(self, db: Database):
        self.db = db

    def add_production(self, production: ProductionDto):
        query = """
            insert into production (production_code, product_id, quantity, unit, status)
            values (%s, %s, %s, %s, %s) returning production_id, production_code;
        """
        params = (
            production.production_code,
            production.product_id,
            production.quantity,
            production.unit,
            production.status,
        )

        return self.db.execute(query, params)

    def update_production_status(self, production_id: int, status: ProductionStatus):
        query = "update production set status = %s::text where production_id = %s returning production_id, status;"
        return self.db.execute(query, (status, production_id))

    def get_production_status(self, production_id: int):
        query = "select status from production where production_id = %s;"
        return self.db.fetch_one(query, (production_id,))

    def add_proudct_lot(self, lot: ProductLotDto):
        query = """
            insert into product_lot (lot_no, production_id)
            values (%s, %s) 
            returning product_lot_id, lot_no;
        """
        params = (lot.lot_no, lot.production_id)
        return self.db.execute(query, params)

    def add_production_material(self, productionMaterial: ProductionMaterialDto):
        query = """
            insert into production_material (production_id, material_id, quantity, unit)
            values (%s, %s, %s, %s) returning production_material_id;
        """
        params = (
            productionMaterial.production_id,
            productionMaterial.material_id,
            productionMaterial.quantity,
            productionMaterial.unit,
        )
        return self.db.execute(query, params)

    def get_row_count_by_product_lot_no(self, lot_no: str):
        query = "select count(*) from product_lot where lot_no = %s::text;"

        count = self.db.get_row_count(query, (lot_no,))
        return count

    def find_all_production(self):
        query = """
                select 
                    pn.production_id, pl.lot_no, pn.produced_at, 
                    p.product_name, p.product_type,
                    pn.production_code, pn.quantity, pn.unit, pn.status
                from production pn
                join product p
                on p.product_id = pn.product_id
                left join product_lot pl
                on pl.production_id  = pn.production_id
                order by pn.produced_at desc;
            """
        return self.db.fetch_all(query)

    def get_quantity_by_date(self, start: str, end: str):
        query = """
            select produced_at, quantity from production 
            where produced_at between %s and %s
            order by produced_at;
        """
        return self.db.fetch_all(query, (start, end))

    def find_product_by_product_lot(self, lot_no: str):
        count = self.get_row_count_by_product_lot_no(lot_no)

        if count > 0:
            query = """
                select
                    pl.lot_no, p.product_id, p.product_code,
                    p.product_name, p.product_type,
                    pn.production_id, pn.production_code,
                    pn.quantity, pn.unit, pn.produced_at
                from product_lot pl
                join production pn
                on pl.production_id = pn.production_id
                join product p
                on pn.product_id = p.product_id
                where pl.lot_no = %s::text;
            """
            return self.db.fetch_one(query, (lot_no,))

    def find_input_material_by_production(self, production_id: int):
        query = """
            select
                pm.material_id, m.material_name, m.category,
                pm.production_id, pn.quantity, pn.produced_at
            from production_material pm
            join material m
            on pm.material_id = m.material_id
            join production pn
            on pm.production_id = pn.production_id
            where pn.production_id = %s;
        """
        return self.db.fetch_all(query, (production_id,))
