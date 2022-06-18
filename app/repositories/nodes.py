from typing import Optional
from uuid import UUID
from ..models.ShopUnit import ShopUnitSelect, ShopUnit
from ..db.shop_unit import shop_unit
from .base import BaseRepository
from ..models.ShopUnitType import ShopUnitType
from .children import ChildrenRepository
from .shop_unit import ShopUnitRepository


class NodesRepository(BaseRepository):
    async def get_by_id(self, id: UUID) -> Optional[ShopUnit]:
        query = shop_unit.select().where(shop_unit.c.id == id)
        res = await self.database.fetch_one(query)
        if res is None:
            return None
        obj = ShopUnitSelect.parse_obj(res)
        children_repository = ChildrenRepository(self.database)
        shop_unit_repository = ShopUnitRepository(self.database)
        response = ShopUnit(
            id=obj.id,
            name=obj.name,
            date=obj.date,
            type=obj.type,
            price=obj.price if obj.price else None,
            parentId=await children_repository.get_parent_id(obj.id),
            children=await shop_unit_repository.get_children_tree(obj.id),
        )
        if response.type == ShopUnitType.OFFER:
            response.children = None
        return response
