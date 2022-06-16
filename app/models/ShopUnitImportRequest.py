from datetime import datetime
from typing import List
from pydantic import BaseModel, validator
from app.models.ShopUnitImport import ShopUnitImport


class ShopUnitImportRequest(BaseModel):
    items: List[ShopUnitImport]
    updateDate: datetime

    @validator('updateDate')
    def datetime_valid(cls, dt_str: datetime):
        try:
            dt_str.isoformat()
        except:
            raise ValueError('Validation Failed')
        return dt_str.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    @validator('items')
    def items_valid(cls, items: List[ShopUnitImport]):
        items_id_list = []
        for item in items:
            if item.id not in items_id_list:
                items_id_list.append(item.id)
            else:
                raise ValueError('Duplicate id in import items')
        return items
