from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, validator
from app.models.ShopUnitType import ShopUnitType


class ShopUnitStatisticUnit(BaseModel):
    id: UUID
    name: str
    parentId: Optional[UUID] = None
    type: ShopUnitType
    price: int
    date: datetime

    @validator('date')
    def datetime_valid(cls, dt_str: datetime):
        try:
            dt_str.isoformat()
        except:
            raise ValueError('Validation Failed')
        return dt_str.strftime("%Y-%m-%dT%H:%M:%S.000Z")
