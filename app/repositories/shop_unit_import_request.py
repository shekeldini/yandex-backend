from typing import List, Optional

from ..models.ShopUnitImportRequest import ShopUnitImportRequest
from ..models.ShopUnitType import ShopUnitType
from ..db.shop_unit_type import shop_unit_type
from .base import BaseRepository


class ShopUnitImportRequestRepository(BaseRepository):
    async def create(self, shop_unit_items: ShopUnitImportRequest):
        print(shop_unit_items)
        return


