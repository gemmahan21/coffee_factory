from dataclasses import dataclass

from .enum import ProductType, ProductionStatus, MaterialCategory


@dataclass
class MaterialDto:
    material_code: str
    material_name: str
    category: MaterialCategory


@dataclass
class ProductDto:
    product_code: str
    product_name: str
    product_type: ProductType
    is_active: str


@dataclass
class ProductionDto:
    production_code: str
    product_id: int
    quantity: int
    unit: str
    status: ProductionStatus


@dataclass
class ProductLotDto:
    lot_no: str
    production_id: int


@dataclass
class ProductionMaterialDto:
    production_id: int
    material_id: int
    quantity: int
    unit: str
