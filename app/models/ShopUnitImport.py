from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from app.models.ShopUnitType import ShopUnitType


class ShopUnitImport(BaseModel):
    id: UUID
    name: str
    parentId: Optional[UUID] = None
    type: ShopUnitType
    price: int

