from typing import Optional
from uuid import UUID
from pydantic import BaseModel, root_validator
from app.models.ShopUnitType import ShopUnitTypeEnum


class ShopUnitImport(BaseModel):
    id: UUID
    name: str
    parentId: Optional[UUID] = None
    type: ShopUnitTypeEnum
    price: Optional[int] = None

    @root_validator
    def price_validation(cls, values):
        type, price = values.get("type"), values.get("price")
        if type.value == ShopUnitTypeEnum.CATEGORY.value and price:
            raise ValueError('Validation Failed')
        if type.value == ShopUnitTypeEnum.OFFER.value and (not price or price < 0):
            raise ValueError('Validation Failed')
        return values
