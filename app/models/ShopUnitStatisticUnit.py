from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, validator

from app.core.config import DATE_TIME_FORMAT
from app.models.ShopUnitType import ShopUnitType


class ShopUnitStatisticUnit(BaseModel):
    id: UUID
    name: str
    parentId: Optional[UUID] = None
    type: ShopUnitType
    price: Optional[int] = None
    date: datetime

    @validator('date')
    def datetime_valid(cls, date: datetime):
        try:
            date.isoformat()
        except:
            raise ValueError('Validation Failed')
        return date.strftime(date.strftime(DATE_TIME_FORMAT))
