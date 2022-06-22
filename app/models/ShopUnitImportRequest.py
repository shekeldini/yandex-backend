from datetime import datetime
from typing import List
from pydantic import BaseModel, validator
from app.models.ShopUnitImport import ShopUnitImport


class ShopUnitImportRequest(BaseModel):
    items: List[ShopUnitImport]
    updateDate: datetime

    @validator('updateDate')
    def datetime_valid(cls, date: datetime):
        """
        Try convert date to iso format

        If can't raise 'Validation Failed' exception

        Else return date
        """
        try:
            date.isoformat()
        except:
            raise ValueError('Validation Failed')
        return date

    @validator('items')
    def items_valid(cls, items: List[ShopUnitImport]):
        """
        Find duplicate id in items

        If found raise 'Duplicate id in import items' exception

        Else return items
        """
        items_id_list = []
        for item in items:
            if item.id not in items_id_list:
                items_id_list.append(item.id)
            else:
                raise ValueError('Duplicate id in import items')
        return items
