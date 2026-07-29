from datetime import date
import calendar

from .database import Database
from .repository import ProductionRepository
from .enum import ProductionStatus, MaterialCategory, ProductType
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
        return production_repository.add_production_material(production_material)
    else:
        return None


def create_product_lot(
    production_repository: ProductionRepository, product_lot: ProductLotDto
):
    response = production_repository.get_production_status(product_lot.production_id)

    if response.get("status") == ProductionStatus.COMPLETED:
        return production_repository.add_proudct_lot(product_lot)
    else:
        return None


def validate_number(str: str):
    if str.isdigit():
        validated_num = int(str)
        return validated_num
    else:
        return 0


def get_current_date():
    year = date.today().year
    month = date.today().month
    _, last_day = calendar.monthrange(year, month)

    current_date = {
        "start": date(year, month - 2, 1),
        "end": date(year, month, last_day),
    }

    return current_date


def get_today_str():
    return str(date.today()).replace("-", "")


def generate_code(type: str):
    if type == "production":
        return f"PROD-{get_today_str()}-001"
    elif type == "product_lot":
        return f"LOT-FG-{get_today_str()}-001"
    else:
        return get_today_str()


def genarate_material_code(category: MaterialCategory):
    code = "MAT-"
    if category == MaterialCategory.GREEN_BEAN:
        code = code + MaterialCategory.GREEN_BEAN.split("_")[1]
    elif category == MaterialCategory.MILK_POWDER:
        code = code + MaterialCategory.MILK_POWDER.split("_")[0]
    elif category == MaterialCategory.OTHER:
        pass
    else:
        code = code + category
    return code


def generate_product_code(type: ProductType):
    code = "PRD-"
    if type == ProductType.COFFEE_MIX:
        code += ProductType.COFFEE_MIX.split("_")[1]
    elif type == ProductType.DRIP_COFFEE:
        code += ProductType.DRIP_COFFEE.split("_")[0]
    else:
        code += type
    return code
