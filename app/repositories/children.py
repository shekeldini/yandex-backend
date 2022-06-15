from typing import List, Optional
from uuid import UUID
from ..db.shop_unit import shop_unit
from ..models.Children import Children
from ..db.children import children
from .base import BaseRepository
from ..models.ShopUnit import ShopUnitDB
from ..models.ShopUnitImport import ShopUnitImport


class ChildrenRepository(BaseRepository):
    async def get_all(self) -> List[Children]:
        query = children.select()
        return [Children.parse_obj(row) for row in await self.database.fetch_all(query)]

    async def create(self, item: ShopUnitImport):
        if not item.parentId:
            return None
        new_children = Children(
            children_id=item.id,
            parent_id=item.parentId
        )

        values = {**new_children.dict()}
        query = children.insert().values(**values)
        return await self.database.execute(query)

    async def update(self, item: ShopUnitImport):
        if not item.parentId:
            return None
        update_children = Children(
            children_id=item.id,
            parent_id=item.parentId
        )
        values = {**update_children.dict()}
        query = children.update().where(
            (children.c.children_id == update_children.children_id) &
            (children.c.parent_id == update_children.parent_id)
        ).values(**values)
        return await self.database.execute(query)

    async def get_parent(self, children_id: UUID) -> Optional[ShopUnitDB]:
        query = children.select().where(children.c.children_id == children_id)
        parent_res = await self.database.fetch_one(query)
        if not parent_res:
            return None
        children_item = Children.parse_obj(parent_res)
        query = shop_unit.select().where(shop_unit.c.id == children_item.parent_id)
        return ShopUnitDB.parse_obj(await self.database.fetch_one(query))

    async def get_children_list(self, parent_id: UUID) -> List[Children]:
        query = children.select().where(children.c.parent_id == parent_id)
        return [Children.parse_obj(row) for row in await self.database.fetch_all(query)]

    async def get_parent_id(self, children_id: UUID) -> Optional[UUID]:
        query = children.select().where(children.c.children_id == children_id)
        res = await self.database.fetch_one(query)
        if res is None:
            return None
        obj = Children.parse_obj(res)
        return obj.parent_id

    async def have_children(self, parent_id: UUID) -> bool:
        query = children.select().where(children.c.parent_id == parent_id)
        res = await self.database.fetch_all(query)
        if res:
            return True
        return False
