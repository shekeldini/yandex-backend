from typing import List, Optional
from uuid import UUID
from ..models.Children import Children
from ..db.children import children
from .base import BaseRepository
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

    async def get_root_category_id(self, children_id: UUID) -> UUID:
        async def find_root_category_id(children_id, res):
            parent_id = await self.get_parent_id(children_id)
            if parent_id:
                await find_root_category_id(parent_id, res)
            res.append(children_id)
            return res
        res = await find_root_category_id(children_id, [])
        return res[0]
