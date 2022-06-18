from __future__ import annotations
from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, validator

from app.core.config import DATE_TIME_FORMAT
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
    def datetime_valid(cls, date: datetime):
        try:
            date.isoformat()
        except:
            raise ValueError('Validation Failed')
        return date.strftime(date.strftime(DATE_TIME_FORMAT))


class ShopUnitDB(BaseModel):
    id: UUID
    name: str
    date: datetime
    type: ShopUnitType
    price: Optional[int] = None

    @validator('date')
    def datetime_valid(cls, date: datetime):
        try:
            date.isoformat()
        except:
            raise ValueError('Validation Failed')
        return date.strftime(date.strftime(DATE_TIME_FORMAT))
