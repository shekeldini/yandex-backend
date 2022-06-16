from typing import List, Optional
from pydantic import BaseModel
from app.models.ShopUnitStatisticUnit import ShopUnitStatisticUnit


class ShopUnitStatisticResponse(BaseModel):
    items: Optional[List[ShopUnitStatisticUnit]] = []
