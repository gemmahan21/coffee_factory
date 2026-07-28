from dataclasses import dataclass
from datetime import date

from .enum import ProductType, ProductionStatus, MaterialCategory


@dataclass
class Product:
    product_id: int | None
    product_code: str
    product_name: str
    product_type: ProductType
    is_active: str


@dataclass
class Production:
    production_id: int | None
    production_code: str
    product_id: int
    quantity: int
    produced_at: date
    unit: str
    status: ProductionStatus


@dataclass
class Material:
    material_id: int | None
    material_code: str
    material_name: str
    category: MaterialCategory


@dataclass
class ProductLot:
    product_lot_id: int | None
    lot_no: str
    production_id: int


@dataclass
class ProductionMaterial:
    production_material_id: int | None
    production_id: int
    material_id: int
    quantity: int
    unit: str
