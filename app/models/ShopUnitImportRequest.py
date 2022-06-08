from typing import Optional, List
from pydantic import BaseModel, validator
from app.models.ShopUnitImport import ShopUnitImport
from datetime import datetime


class ShopUnitImportRequest(BaseModel):
    items: List[ShopUnitImport]
    updateDate: datetime

    @validator('updateDate')
    def datetime_valid(cls, dt_str):
        try:
            datetime.fromisoformat(dt_str)
        except:
            raise ValueError('Data Validation Failed')
        return dt_str
