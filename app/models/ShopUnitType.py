from enum import Enum
from pydantic import BaseModel


class ShopUnitTypeEnum(str, Enum):
    OFFER = "OFFER"
    CATEGORY = "CATEGORY"


class ShopUnitType(BaseModel):
    shop_unit_type: ShopUnitTypeEnum

