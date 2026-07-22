from .database import Database
from .repository import ProductionRepository


class QueryService:
    def __init__(self, db: Database, repository: None | ProductionRepository = None):
        self.db = db
        self.repository = repository

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

    def find_product_by_product_lot(self, lot_no: str):
        count = self.repository.find_product_lot_no(lot_no)

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

    def input_material_by_production(self, production_id: int):
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
