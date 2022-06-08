from typing import List
from pydantic import BaseModel
from app.models.ShopUnitStatisticUnit import ShopUnitStatisticUnit


class ShopUnitStatisticResponse(BaseModel):
    items: List[ShopUnitStatisticUnit]
