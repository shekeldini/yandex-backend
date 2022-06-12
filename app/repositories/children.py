from typing import List
from ..models.Children import Children
from ..db.children import children
from .base import BaseRepository
from ..models.ShopUnitImport import ShopUnitImport


class ChildrenRepository(BaseRepository):
    async def get_all(self) -> List[Children]:
        query = children.select()
        return [Children.parse_obj(row) for row in await self.database.fetch_all(query)]

    async def create(self, item: ShopUnitImport):
        new_children = Children(
            children_id=item.id,
            parent_id=item.parentId
        )

        values = {**new_children.dict()}
        query = children.insert().values(**values)
        return await self.database.execute(query)

    async def update(self, item: ShopUnitImport):
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





