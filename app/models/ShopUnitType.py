from enum import Enum
from pydantic import BaseModel


class ShopUnitType(str, Enum):
    OFFER = "OFFER"
    CATEGORY = "CATEGORY"


class ShopUnitTypeOutput(BaseModel):
    shop_unit_type: ShopUnitType

