from typing import Optional
from uuid import UUID
from pydantic import BaseModel, validator
from app.models.ShopUnitType import ShopUnitType


class ShopUnitImport(BaseModel):
    id: UUID
    name: str
    parentId: Optional[UUID] = None
    type: ShopUnitType
    price: Optional[int] = None

    @validator('price')
    def price_validation(cls, type, price):
        if type == ShopUnitType.choice.CATEGORY and price:
            raise ValueError('Validation Failed')
        if type == ShopUnitType.choice.OFFER and (not price or price < 0):
            raise ValueError('Validation Failed')
        return price
