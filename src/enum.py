from enum import Enum


class ProductType(str, Enum):
    AMERICANO = "AMERICANO"
    LATTE = "LATTE"
    COFFEE_MIX = "COFFEE_MIX"
    DRIP_COFFEE = "DRIP_COFFEE"


class ProductionStatus(str, Enum):
    PLANNED = "PLANNED"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"
    IN_PROGRESS = "IN_PROGRESS"


class MaterialCategory(str, Enum):
    GREEN_BEAN = "GREEN_BEAN"
    SUGAR = "SUGAR"
    CREAMER = "CREAMER"
    MILK_POWDER = "MILK_POWDER"
    OTHER = "OTHER"
