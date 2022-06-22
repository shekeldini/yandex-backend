from typing import Optional
from uuid import UUID
from ..models.ShopUnit import ShopUnitSelect, ShopUnit
from ..db.shop_unit import shop_unit
from .base import BaseRepository
from ..models.ShopUnitType import ShopUnitType
from .children import ChildrenRepository
from .shop_unit import ShopUnitRepository


class NodesRepository(BaseRepository):
    """
    Class NodesRepository for create nodes/{id} response
        Methods
            -get_by_id(id: UUID)
                return nodes response for shop unit item
    """
    async def get_by_id(self, id: UUID) -> ShopUnit:
        """Create Shop Unit tree"""
        query = shop_unit.select().where(shop_unit.c.id == id)
        # get ShopUnitSelect item from database
        obj = ShopUnitSelect.parse_obj(await self.database.fetch_one(query))
        children_repository = ChildrenRepository(self.database)
        shop_unit_repository = ShopUnitRepository(self.database)
        # find children for category type item. offer can't have children
        if obj.type == ShopUnitType.CATEGORY.value:
            children = await shop_unit_repository.get_children_tree(obj.id)
        else:
            children = None
        response = ShopUnit(
            id=obj.id,
            name=obj.name,
            date=obj.date,
            type=obj.type,
            price=None if obj.price is None else obj.price,
            parentId=await children_repository.get_parent_id(obj.id),
            children=children,
        )
        return response
