from typing import Optional
from uuid import UUID
from pydantic import BaseModel, root_validator
from app.models.ShopUnitType import ShopUnitType


class ShopUnitImport(BaseModel):
    id: UUID
    name: str
    parentId: Optional[UUID] = None
    type: ShopUnitType
    price: Optional[int] = None

    @root_validator
    def price_validation(cls, values):
        type, price = values.get("type"), values.get("price")
        if type.value == ShopUnitType.CATEGORY.value and price:
            raise ValueError('Validation Failed')
        if type.value == ShopUnitType.OFFER.value and (not price or price < 0):
            raise ValueError('Validation Failed')
        return values
