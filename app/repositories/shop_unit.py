from datetime import datetime
from typing import Optional, List
from uuid import UUID
from .children import ChildrenRepository
from app.core.exception import ParentNotFound, OfferCanNotBeParent
from ..db.statistic import statistic
from ..db.children import children
from ..models.Children import Children
from ..models.ShopUnit import ShopUnitInsert, ShopUnit, ShopUnitSelect, ShopUnitDump
from ..db.shop_unit import shop_unit
from .base import BaseRepository
from ..models.ShopUnitImport import ShopUnitImport
from ..models.ShopUnitType import ShopUnitType


class ShopUnitRepository(BaseRepository):
    """
        A class ShopUnitRepository for work with shop_unit table in database

        Methods
            -get_by_id(id: UUID)
                get shop_unit item from database if exist
            -get_price(id: UUID)
                get price shop_unit item by id
            -get_all_parents_for_parent(child_id: UUID, updated_id: list)
                get parent list
            -update_date(id: UUID, date: datetime)
                update date for category and create dump in table statistic
            -create(item: ShopUnitImport, date: datetime)
                create new shop unit item
                and create record in children table if item has parentId
                and create dump in table statistic
            -update(item: ShopUnitImport, date: datetime, dump=True, update_price=False)
                update shop unit item
                and create dump in table statistic if dump=True
                and update category price if need (using for update_parent_price)
            -delete(id: UUID)
                delete shop unit item if exist and all children
            -create_dump(id: UUID, name: str, date: datetime, parentId: UUID, price: Optional[int], type: str)
                create dump record in table statistic
            -get_children_tree(id: UUID)
                create children tree for parentId
            -update_parent_price(id: UUID)
                update root parent and all child category price
        """

    async def get_by_id(self, id: UUID) -> Optional[ShopUnitSelect]:
        """Get shop_unit item from database if exist"""
        query = shop_unit.select().where(shop_unit.c.id == id)
        res = await self.database.fetch_one(query)
        if res is None:
            return None
        return ShopUnitSelect.parse_obj(res)

    async def get_price(self, id: UUID) -> Optional[int]:
        """Get price shop_unit item by id"""

        query = """
        SELECT price FROM shop_unit 
        WHERE id = :id
        """
        values = {"id": id}
        res = await self.database.execute(query=query, values=values)
        if res is None:
            return None
        return res

    async def get_all_parents_for_parent(self, child_id: UUID, updated_id: list):
        """Get parent list"""
        # add child_id in updated_id list
        updated_id.append(child_id)
        query = children.select().where(children.c.children_id == child_id)
        # find parent for child
        res = await self.database.fetch_one(query)
        if res:
            child = Children.parse_obj(res)
            # if parent found recursive find parent
            # do it before found root parent without child
            await self.get_all_parents_for_parent(child.parent_id, updated_id)
        # return list with id parents
        return updated_id

    async def update_date(self, id: UUID, date: datetime):
        """Update date for category and create dump in table statistic"""
        # get old item from database
        item = await self.get_by_id(id)
        # create new item model
        update_data = ShopUnitInsert(
            id=item.id,
            name=item.name,
            date=date,
            type=item.type,
            price=item.price
        )
        # convert model to dict
        values = {**update_data.dict()}
        # remove id from dict
        values.pop("id", None)
        query = shop_unit.update().where(shop_unit.c.id == update_data.id).values(**values)
        # update item
        return await self.database.execute(query=query)


    async def create(self, item: ShopUnitImport, date: datetime):
        """
        Create new shop unit item
        and create record in children table if item has parentId
        and create dump in table statistic
        """
        # Create model ShopUnitInsert from item: ShopUnitImport and date: datetime
        new_shop_unit_item = ShopUnitInsert(
            id=item.id,
            name=item.name,
            date=date,
            type=item.type,
            price=item.price
        )
        # convert model to dict
        values = {**new_shop_unit_item.dict()}
        # create query using sqlalchemy
        query = shop_unit.insert().values(**values)
        children_repository = ChildrenRepository(self.database)
        # check item.parentId
        if item.parentId:
            # get parent item
            parent = await self.get_by_id(item.parentId)
            if not parent:
                # if parent not found raise ParentNotFound exception
                raise ParentNotFound()
            if parent.type != ShopUnitType.CATEGORY.value:
                # if parent.type is OFFER raise OfferCanNotBeParent exception
                raise OfferCanNotBeParent()
            # create new item
            await self.database.execute(query)
            # create record i
            await children_repository.create(item)
        else:
            # create new item if item.parentId is None
            await self.database.execute(query)

    async def update(self, item: ShopUnitImport, date: datetime, update_price=False):
        """
        Update shop unit item
        and create dump in table statistic if dump=True
        and update category price if need (using for update_parent_price)
        """
        # Create model ShopUnitInsert from item: ShopUnitImport and date: datetime
        update_shop_unit_item = ShopUnitInsert(
            id=item.id,
            name=item.name,
            date=date,
            type=item.type,
            price=item.price
        )
        # convert model to dict
        values = {**update_shop_unit_item.dict()}
        # remove "id" from dict
        values.pop("id", None)
        # if we update CATEGORY we remove values.price if update_price is False.
        # update_price=True then we calculate category price
        if not update_price and update_shop_unit_item.type.value == ShopUnitType.CATEGORY.value:
            values.pop("price", None)
        # update item
        query = shop_unit.update().where(shop_unit.c.id == update_shop_unit_item.id).values(**values)
        await self.database.execute(query=query)

        children_repository = ChildrenRepository(self.database)
        # get old parentId
        parent_id = await children_repository.get_parent_id(item.id)
        # old parentId is None and we have new parentId
        if not parent_id and item.parentId:
            # create new parent for item
            await children_repository.create(item)
            # update new parent price
            await self.update_parent_price(item.parentId)
        # new parentId is None
        elif parent_id and item.parentId is None:
            await children_repository.delete(item.id)
            await self.update_parent_price(parent_id)
        # old parentId don't match with new parentId
        elif item.parentId and parent_id != item.parentId:
            # update parentId for item
            await children_repository.update(item)
            # update price for new parentId
            await self.update_parent_price(item.parentId)
            # update price for old parentId
            await self.update_parent_price(parent_id)
        return

    async def delete(self, id: UUID):
        """ Recursive delete shop unit item if exist and all children"""
        query = children.select().where(children.c.parent_id == id)
        # Get children list
        children_list = [Children.parse_obj(row) for row in await self.database.fetch_all(query)]
        if children_list:
            for child in children_list:
                # if children list is not empty recursive call func delete with child.id
                await self.delete(child.children_id)
        # if item don't have children -> delete this item
        query = shop_unit.delete().where(shop_unit.c.id == id)
        return await self.database.execute(query=query)

    async def create_dump(self, id: UUID):
        """Create dump record in table statistic"""
        item = await self.get_by_id(id)
        children_repository = ChildrenRepository(self.database)
        # create dump model
        new_dump = ShopUnitDump(
            id=id,
            name=item.name,
            date=item.date,
            parent_id=await children_repository.get_parent_id(item.id),
            price=item.price,
            type=item.type
        )
        # convert model to dict
        values = {**new_dump.dict()}
        # create query using sqlalchemy
        query = statistic.insert().values(**values)
        # execute script
        return await self.database.execute(query)

    async def get_children_tree(self, id: UUID) -> List[ShopUnit]:
        """Create children tree for parentId"""
        res = []
        children_repository = ChildrenRepository(self.database)

        async def get_children_for_parent(parent_id, res):
            """recursive find children for parent"""
            nonlocal children_repository
            # find children for parent
            children_list = await children_repository.get_children_list(parent_id)
            if children_list:
                for item in children_list:
                    # get children item from database
                    children_obj = ShopUnitSelect.parse_obj(await self.get_by_id(item.children_id))
                    is_category = children_obj.type == ShopUnitType.CATEGORY.value
                    node = ShopUnit(
                        id=children_obj.id,
                        name=children_obj.name,
                        type=children_obj.type,
                        price=children_obj.price,
                        date=children_obj.date,
                        parentId=item.parent_id,
                        children=[]
                    ).dict()
                    # add child in list
                    res.append(node)
                    # if child is category recursive call function get_children_for_parent and find children
                    if is_category:
                        await get_children_for_parent(res[-1]["id"], res[-1]["children"])
                    # else child type OFFER he has no children
                    else:
                        res[-1]["children"] = None

        # call func and fill res
        await get_children_for_parent(id, res)
        # return complete res list
        return res

    async def update_parent_price(self, id: UUID):
        """Update root parent and all child category price"""

        async def mean_list(my_list: list):
            """return mean of list"""
            return sum(my_list) // len(my_list) if my_list else None

        async def update(root: ShopUnit):
            """recursive update category price"""
            offer_for_node = []
            for node in root.children:
                if node.type == "OFFER":
                    offer_for_node.append(node.price)
                if node.type == "CATEGORY":
                    offer_for_node += await update(node)

            update_item = ShopUnitImport.unvalidated(
                id=root.id,
                name=root.name,
                parentId=root.parentId,
                type=root.type,
                price=await mean_list(offer_for_node)
            )
            await self.update(update_item, root.date, update_price=True)
            return offer_for_node

        children_repository = ChildrenRepository(self.database)
        # find root parentId
        root_category_id = await children_repository.get_root_category_id(id)
        # find record in database
        item = await self.get_by_id(root_category_id)
        # create children tree
        children_list = await self.get_children_tree(root_category_id)
        # create node
        data = ShopUnit.parse_obj({**item.dict(), "children": children_list})
        # update root price and children category price
        return await update(data)
