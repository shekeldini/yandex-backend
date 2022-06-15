from typing import Optional, List
from uuid import UUID
from .children import ChildrenRepository
from ..db.children import children
from ..models.Children import Children
from ..models.ShopUnit import ShopUnitDB, ShopUnit
from ..db.shop_unit import shop_unit
from .base import BaseRepository
from ..models.ShopUnitImport import ShopUnitImport
from ..models.ShopUnitType import ShopUnitType


class ShopUnitRepository(BaseRepository):
    async def get_by_id(self, id: UUID) -> Optional[ShopUnitDB]:
        query = shop_unit.select().where(shop_unit.c.id == id)
        res = await self.database.fetch_one(query)
        if res is None:
            return None
        return ShopUnitDB.parse_obj(res)

    async def update_parent(self, child_id: UUID, date: str):
        query = children.select().where(children.c.children_id == child_id)
        res = await self.database.fetch_one(query)
        if res:
            child = Children.parse_obj(res)
            await self.update_parent(child.parent_id, date)
        item = await self.get_by_id(child_id)
        return await self.update_date(item, date)

    async def update_date(self, item: ShopUnitDB, date: str):

        update_data = ShopUnitDB(
            id=item.id,
            name=item.name,
            date=date,
            type=item.type,
            price=item.price
        )
        values = {**update_data.dict()}
        values.pop("id", None)
        query = shop_unit.update().where(shop_unit.c.id == update_data.id).values(**values)
        return await self.database.execute(query=query)

    async def create(self, item: ShopUnitImport, date: str):
        new_shop_unit_item = ShopUnitDB(
            id=item.id,
            name=item.name,
            date=date,
            type=item.type,
            price=item.price
        )
        values = {**new_shop_unit_item.dict()}
        query = shop_unit.insert().values(**values)
        await self.database.execute(query)
        children_repository = ChildrenRepository(self.database)
        await children_repository.create(item)
        return

    async def update(self, item: ShopUnitImport, date: str):
        update_shop_unit_item = ShopUnitDB(
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
        await children_repository.update(item)
        return

    async def delete(self, id: UUID):
        query = children.select().where(children.c.parent_id == id)
        children_list = [Children.parse_obj(row) for row in await self.database.fetch_all(query)]
        if children_list:
            for child in children_list:
                await self.delete(child.children_id)
        query = shop_unit.delete().where(shop_unit.c.id == id)

        return await self.database.execute(query=query)

    async def get_children_tree(self, id: UUID) -> List[ShopUnit]:
        res = []
        children_repository = ChildrenRepository(self.database)

        async def get_children_for_parent(parent_id, res):
            nonlocal children_repository
            children_list = await children_repository.get_children_list(parent_id)
            if children_list:
                for item in children_list:
                    children_obj = ShopUnitDB.parse_obj(await self.__get_by_id_from_db(item.children_id))
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

    async def update_price(self, id: UUID):
        price = await self.__calculate_price(id)
        query = shop_unit.update().where(shop_unit.c.id == id).values(price=price)
        await self.database.execute(query=query)
        children_repository = ChildrenRepository(self.database)
        parent = await children_repository.get_parent(id)
        if parent:
            await self.update_price(parent.id)
        return

    async def __get_by_id_from_db(self, id: UUID) -> Optional[ShopUnitDB]:
        query = shop_unit.select().where(shop_unit.c.id == id)
        res = await self.database.fetch_one(query)
        if res is None:
            return None
        obj = ShopUnitDB.parse_obj(res)
        return obj

    async def __calculate_price(self, id: UUID) -> Optional[int]:
        def get_all_offers(root: dict, offer_list: list):
            if root["children"]:
                for node in root["children"]:
                    if node["type"] == "CATEGORY":
                        get_all_offers(node, offer_list)
            for node in root["children"]:
                if node["type"] == "OFFER":
                    offer_list.append(node["price"])
            return offer_list

        def mean_list(my_list: list) -> Optional[int]:
            return sum(my_list) // len(my_list) if my_list else None

        item = await self.get_by_id(id)
        children = await self.get_children_tree(id)
        return mean_list(get_all_offers({**item.dict(), "children": children }, []))
