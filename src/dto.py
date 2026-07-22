from dataclasses import dataclass


@dataclass
class MaterialDto:
    material_code: str
    material_name: str
    category: str


@dataclass
class ProductDto:
    product_code: str
    product_name: str
    product_type: str
    is_active: str


@dataclass
class ProductionDto:
    production_code: str
    product_id: int
    quantity: int
    unit: str
    status: str


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
