from .database import Database
from .repository import ProductionRepository
from .enum import ProductionStatus
from .dto import ProductionMaterialDto, ProductLotDto


def connect_db():
    try:
        db = Database()
        return db
    except RuntimeError as e:
        print(f"DB connect Error : {e}")


def input_production_material(
    production_repository: ProductionRepository,
    production_material: ProductionMaterialDto,
):
    response = production_repository.get_production_status(
        production_material.production_id
    )

    if response.get("status") == ProductionStatus.IN_PROGRESS:
        production_repository.add_production_material(production_material)


def create_product_lot(
    production_repository: ProductionRepository, product_lot: ProductLotDto
):
    response = production_repository.get_production_status(product_lot.production_id)

    if response.get("status") == ProductionStatus.COMPLETED:
        production_repository.add_proudct_lot(product_lot.lot_no)


def validate_number(str: str):
    if str.isdigit():
        validated_num = int(str)
        return validated_num
    else:
        return 0
