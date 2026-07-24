from .repository import ProductionRepository

from .dto import ProductionDto, ProductLotDto, ProductionMaterialDto
from .enum import ProductionStatus


class ProductionService:
    def __init__(self, repository: ProductionRepository):
        self.repository = repository

    def add_production(self, production: ProductionDto):
        self.repository.add_production(production)

    def update_production_status(self, production_id: int, status: ProductionStatus):
        self.repository.update_production_status(production_id, status)

    def add_proudct_lot(self, lot: ProductLotDto):
        self.repository.add_proudct_lot(lot)

    def add_production_material(self, productionMaterial: ProductionMaterialDto):
        self.repository.add_production_material(productionMaterial)

    def find_all_production(self):
        return self.repository.find_all_production()

    def get_row_count_by_product_lot_no(self, lot_no: str):
        return self.repository.get_row_count_by_product_lot_no(lot_no)

    def find_product_by_product_lot(self, lot_no: str):
        count = self.get_row_count_by_product_lot_no(lot_no)

        if count > 0:
            return self.find_product_by_product_lot(lot_no)
        else:
            return []

    def find_input_material_by_production(self, production_id: int):
        return self.repository.find_input_material_by_production(production_id)
