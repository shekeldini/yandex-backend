from __future__ import annotations
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, validator
from app.models.ShopUnitType import ShopUnitType


class ShopUnit(BaseModel):
    id: UUID
    name: str
    date: datetime
    parentId: Optional[UUID] = None
    type: ShopUnitType
    price: Optional[int] = None
    children: Optional[List[ShopUnit]] = None

    @validator('date')
    def datetime_valid(cls, dt_str: datetime):
        try:
            dt_str.isoformat()
        except:
            raise ValueError('Validation Failed')
        return dt_str.strftime("%Y-%m-%dT%H:%M:%S.000Z")


class ShopUnitDB(BaseModel):
    id: UUID
    name: str
    date: datetime
    type: ShopUnitType
    price: Optional[int] = None

    @validator('date')
    def datetime_valid(cls, dt_str: datetime):
        try:
            dt_str.isoformat()
        except:
            raise ValueError('Validation Failed')
        return dt_str.strftime("%Y-%m-%dT%H:%M:%S.000Z")