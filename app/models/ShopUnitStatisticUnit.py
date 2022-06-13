from typing import Optional
from uuid import UUID
from pydantic import BaseModel, validator
from app.models.ShopUnitType import ShopUnitType
from dateutil import parser


class ShopUnitStatisticUnit(BaseModel):
    id: UUID
    name: str
    parentId: Optional[UUID] = None
    type: ShopUnitType
    price: int
    date: str

    @validator('updateDate')
    def datetime_valid(cls, dt_str):
        try:
            parser.parse(dt_str)
        except:
            raise ValueError('Validation Failed')
        return dt_str
