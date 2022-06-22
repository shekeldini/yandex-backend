from typing import List, Optional
from uuid import UUID
from ..models.Children import Children
from ..db.children import children
from .base import BaseRepository
from ..models.ShopUnitImport import ShopUnitImport


class ChildrenRepository(BaseRepository):
    """
    A class ChildrenRepository for work with children table in database

    Methods
        create(item: ShopUnitImport)
            create relation children_id - parent_id
        get_children_list(parent_id: UUID)
            get children list for parent
        get_parent_id(children_id: UUID)
            get parent id for children
        get_root_category_id(children_id: UUID)
            get root parent id
        update(item: ShopUnitImport)
            update parent for child
        delete(id: UUID)
            delete parent for child

    """
    async def create(self, item: ShopUnitImport):
        """
        Create relation children_id - parent_id
        """
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
        """
        Get children list for parent
        """
        query = children.select().where(children.c.parent_id == parent_id)
        return [Children.parse_obj(row) for row in await self.database.fetch_all(query)]

    async def get_parent_id(self, children_id: UUID) -> Optional[UUID]:
        """
        Get parent id for children
        """
        query = children.select().where(children.c.children_id == children_id)
        res = await self.database.fetch_one(query)
        if res is None:
            return None
        obj = Children.parse_obj(res)
        return obj.parent_id

    async def get_root_category_id(self, children_id: UUID) -> UUID:
        """
        Get root parent id
        """
        async def find_root_category_id(children_id, res):
            """
            Find root category id and append in res: list
            """
            parent_id = await self.get_parent_id(children_id)
            if parent_id:
                await find_root_category_id(parent_id, res)
            res.append(children_id)
            return res
        res = await find_root_category_id(children_id, [])
        return res[0]

    async def update(self, item: ShopUnitImport):
        """
        update parent for child
        """
        new_children = Children(
            children_id=item.id,
            parent_id=item.parentId
        )

        values = {**new_children.dict()}
        query = children.update().where(children.c.children_id == item.id).values(**values)
        return await self.database.execute(query)

    async def delete(self, id: UUID):
        """
        delete parent for child
        """
        query = children.delete().where(children.c.children_id == id)
        return await self.database.execute(query)