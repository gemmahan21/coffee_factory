from .database import Database


class QueryService:
    def __init__(self, db: Database):
        self.db = db

    def find_all_production(self):
        query = """
            select 
                p.product_id, p.product_name, p.product_type,
                pn.production_id, pn.production_code, 
                pn.quantity, pn.unit, pn.status, pn.produced_at
            from production pn
            join product p
            on p.product_id = pn.product_id;
        """
        return self.db.fetch_all(query)

    def find_input_material_by_production(self, production_id: int):
        query = """
            select
                m.material_id, m.material_name, m.category,
                m.quantity, m.unit,
                pn.productiono_id, pn.quantity, pn.produced_at
            from product_material pm
            join material m
            on pm.material_id = m.material_id
            join production pn
            on pm.production_id = pn.production_id
            where production_id = %s;
        """
        self.db.fetch_one(query, (production_id,))

    def find_product_lot(self):
        pass
