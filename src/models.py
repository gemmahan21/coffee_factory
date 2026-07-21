from dataclasses import dataclass


@dataclass
class Product:
    product_id: int
    product_code: str
    product_name: str
    product_type: str
    is_active: str


@dataclass
class Production:
    production_id: int
    production_code: str
    product_id: int
    quantity: int
    unit: str
    status: str


@dataclass
class Product_lot:
    product_lot_id: int
    lot_no: str
    production_id: int
    produced_at: str


@dataclass
class Material:
    material_id: int
    material_code: str
    material_name: str
    category: str


@dataclass
class Production_material:
    production_material_id: int
    production_id: int
    material_id: int
