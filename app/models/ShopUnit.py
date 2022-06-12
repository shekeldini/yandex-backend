from __future__ import annotations
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, validator
from datetime import datetime
from app.models.ShopUnitType import ShopUnitType


class ShopUnit(BaseModel):
    id: UUID
    name: str
    date: datetime
    parentId: Optional[UUID] = None
    type: ShopUnitType
    price: int
    children: Optional[ShopUnit] = None

    @validator('date')
    def datetime_valid(cls, dt_str):
        try:
            datetime.fromisoformat(str(dt_str))
        except:
            raise ValueError('Validation Failed')
        return dt_str


class ShopUnitDB(BaseModel):
    id: UUID
    name: str
    date: str
    shop_unit_type: ShopUnitType
    price: Optional[int] = None
