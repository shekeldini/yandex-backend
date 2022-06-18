from datetime import datetime
from typing import Optional, List
from uuid import UUID
from .children import ChildrenRepository
from ..db.statistic import statistic
from ..db.children import children
from ..models.Children import Children
from ..models.ShopUnit import ShopUnitInsert, ShopUnit, ShopUnitSelect, ShopUnitDump
from ..db.shop_unit import shop_unit
from .base import BaseRepository
from ..models.ShopUnitImport import ShopUnitImport
from ..models.ShopUnitType import ShopUnitType


class ShopUnitRepository(BaseRepository):
    async def get_by_id(self, id: UUID) -> Optional[ShopUnitSelect]:
        query = shop_unit.select().where(shop_unit.c.id == id)
        res = await self.database.fetch_one(query)
        if res is None:
            return None
        return ShopUnitSelect.parse_obj(res)

    async def get_all_parents_for_parent(self, child_id: UUID, updated_id: list):
        updated_id.append(child_id)
        query = children.select().where(children.c.children_id == child_id)
        res = await self.database.fetch_one(query)
        if res:
            child = Children.parse_obj(res)
            await self.get_all_parents_for_parent(child.parent_id, updated_id)

        return updated_id

    async def update_date(self, id: UUID, date: datetime):
        item = await self.get_by_id(id)
        update_data = ShopUnitInsert(
            id=item.id,
            name=item.name,
            date=date,
            type=item.type,
            price=item.price
        )
        values = {**update_data.dict()}
        values.pop("id", None)
        query = shop_unit.update().where(shop_unit.c.id == update_data.id).values(**values)
        await self.database.execute(query=query)
        children_repository = ChildrenRepository(self.database)
        return await self.create_dump(
            id=item.id,
            name=item.name,
            date=date,
            parentId=await children_repository.get_parent_id(item.id),
            price=item.price,
            type=item.type
        )

    async def create(self, item: ShopUnitImport, date: datetime):
        new_shop_unit_item = ShopUnitInsert(
            id=item.id,
            name=item.name,
            date=date,
            type=item.type,
            price=item.price
        )
        values = {**new_shop_unit_item.dict()}
        query = shop_unit.insert().values(**values)
        await self.database.execute(query)
        if item.parentId:
            children_repository = ChildrenRepository(self.database)
            await children_repository.create(item)
        children_repository = ChildrenRepository(self.database)
        return await self.create_dump(
            id=item.id,
            name=item.name,
            date=date,
            parentId=await children_repository.get_parent_id(item.id),
            price=item.price,
            type=item.type
        )

    async def update(self, item: ShopUnitImport, date: datetime, dump=True):
        update_shop_unit_item = ShopUnitInsert(
            id=item.id,
            name=item.name,
            date=date,
            type=item.type,
            price=item.price
        )
        values = {**update_shop_unit_item.dict()}
        values.pop("id", None)
        query = shop_unit.update().where(shop_unit.c.id == update_shop_unit_item.id).values(**values)
        await self.database.execute(query=query)
        children_repository = ChildrenRepository(self.database)
        if dump:
            await self.create_dump(
                id=item.id,
                name=item.name,
                date=date,
                parentId=await children_repository.get_parent_id(item.id),
                price=item.price,
                type=item.type
            )
        return

    async def delete(self, id: UUID):
        query = children.select().where(children.c.parent_id == id)
        children_list = [Children.parse_obj(row) for row in await self.database.fetch_all(query)]
        if children_list:
            for child in children_list:
                await self.delete(child.children_id)
        query = shop_unit.delete().where(shop_unit.c.id == id)
        return await self.database.execute(query=query)

    async def create_dump(
            self,
            id: UUID,
            name: str,
            date: datetime,
            parentId: UUID,
            price: Optional[int],
            type: str
    ):
        new_dump = ShopUnitDump(
            id=id,
            name=name,
            date=date,
            parentId=parentId,
            price=price,
            type=type
        )
        values = {**new_dump.dict()}
        query = statistic.insert().values(**values)
        return await self.database.execute(query)

    async def get_children_tree(self, id: UUID) -> List[ShopUnit]:
        res = []
        children_repository = ChildrenRepository(self.database)

        async def get_children_for_parent(parent_id, res):
            nonlocal children_repository
            children_list = await children_repository.get_children_list(parent_id)
            if children_list:
                for item in children_list:
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
                    res.append(node)

                    if is_category:
                        await get_children_for_parent(res[-1]["id"], res[-1]["children"])

                    else:
                        res[-1]["children"] = None

        await get_children_for_parent(id, res)
        return res

    async def update_parent_price(self, id: UUID):
        async def mean_list(my_list: list):
            return sum(my_list) // len(my_list) if my_list else 0

        async def merge_list(temp_list, branch_sum):
            res = []
            res += temp_list
            res += branch_sum
            return res

        async def update(root: ShopUnit, sum_list: list, branch_sum_list: list):
            branch_sum_list.clear()
            if root.children:
                for node in root.children:
                    if node.type == "CATEGORY":
                        await update(node, sum_list, branch_sum_list)

            temp_list = []
            for node in root.children:
                if node.type == "OFFER":
                    sum_list.append(node.price)
                    temp_list.append(node.price)
            root_price = await mean_list(await merge_list(temp_list, branch_sum_list))
            update_item = ShopUnitImport.unvalidated(
                id=root.id,
                name=root.name,
                parentId=root.parentId,
                type=root.type,
                price=root_price
            )
            await self.update(update_item, root.date, dump=False)
            await add_in_list_from_another_list(temp_list, branch_sum_list)
            return sum_list

        async def add_in_list_from_another_list(add_from: list, add_to: list):
            for i in add_from:
                add_to.append(i)

        children_repository = ChildrenRepository(self.database)

        root_category_id = await children_repository.get_root_category_id(id)

        item = await self.get_by_id(root_category_id)
        children_list = await self.get_children_tree(root_category_id)
        data = ShopUnit.parse_obj({**item.dict(), "children": children_list})
        root_price = await mean_list(await update(data, [], []))
        update_item = ShopUnitImport.unvalidated(
            id=data.id,
            name=data.name,
            parentId=data.parentId,
            type=data.type,
            price=root_price
        )
        return await self.update(update_item, data.date, dump=False)
