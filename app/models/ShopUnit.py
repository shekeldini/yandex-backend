from __future__ import annotations
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, validator
from app.models.ShopUnitType import ShopUnitType
from dateutil import parser


class ShopUnit(BaseModel):
    id: UUID
    name: str
    date: str
    parentId: Optional[UUID] = None
    type: ShopUnitType
    price: Optional[int] = None
    children: Optional[List[ShopUnit]] = None

    @validator('date')
    def datetime_valid(cls, dt_str):
        try:
            parser.parse(dt_str)
        except:
            raise ValueError('Validation Failed')
        return dt_str


class ShopUnitDB(BaseModel):
    id: UUID
    name: str
    date: str
    shop_unit_type: ShopUnitType
    price: Optional[int] = None

    @validator('date')
    def datetime_valid(cls, dt_str):
        try:
            parser.parse(dt_str)
        except:
            raise ValueError('Validation Failed')
        return dt_str