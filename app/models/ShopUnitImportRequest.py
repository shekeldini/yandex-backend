from typing import List
from pydantic import BaseModel, validator
from app.models.ShopUnitImport import ShopUnitImport
from dateutil import parser


class ShopUnitImportRequest(BaseModel):
    items: List[ShopUnitImport]
    updateDate: str

    @validator('updateDate')
    def datetime_valid(cls, dt_str):
        try:
            parser.parse(dt_str)
        except:
            raise ValueError('Data Validation Failed')
        return dt_str
