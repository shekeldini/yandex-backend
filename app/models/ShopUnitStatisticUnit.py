from typing import Optional
from uuid import UUID
from pydantic import BaseModel, validator
from app.models.ShopUnitType import ShopUnitType
from datetime import datetime


class ShopUnitStatisticUnit(BaseModel):
    id: UUID
    name: str
    parentId: Optional[UUID] = None
    type: ShopUnitType
    price: int
    date: datetime

    @validator('date')
    def datetime_valid(cls, dt_str):
        try:
            datetime.fromisoformat(dt_str)
        except:
            raise ValueError('Data Validation Failed')
        return dt_str

