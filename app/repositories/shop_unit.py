from datetime import datetime
from typing import List, Optional
from uuid import UUID

from ..db.children import children
from ..models.Children import Children
from ..models.ShopUnit import ShopUnitDB, ShopUnit
from ..db.shop_unit import shop_unit
from .base import BaseRepository
from ..models.ShopUnitImport import ShopUnitImport
from ..models.ShopUnitType import ShopUnitType


class ShopUnitRepository(BaseRepository):
    async def __get_children(self, id: UUID) -> List[ShopUnit]:
        res = []

        async def get(id, res):
            query = children.select().where(children.c.parent_id == id)
            children_list = [Children.parse_obj(row) for row in await self.database.fetch_all(query)]
            if children_list:
                for item in children_list:

                    children_obj = ShopUnitDB.parse_obj(await self.__get_by_id_from_db(item.children_id))
                    is_category = children_obj.shop_unit_type == ShopUnitType.CATEGORY.value

                    res.append({})
                    res[-1]["children"] = []
                    res[-1]["id"] = children_obj.id
                    res[-1]["type"] = children_obj.shop_unit_type
                    res[-1]["price"] = children_obj.price
                    res[-1]["name"] = children_obj.name
                    res[-1]["date"] = children_obj.date
                    res[-1]["parentId"] = item.parent_id

                    if is_category:
                        await get(children_obj.id, res[-1]["children"])

                    else:
                        res[-1]["children"] = None

        await get(id, res)
        return res

    async def __get_by_id_from_db(self, id: UUID) -> Optional[ShopUnitDB]:
        query = shop_unit.select().where(shop_unit.c.id == id)
        res = await self.database.fetch_one(query)
        if res is None:
            return None
        obj = ShopUnitDB.parse_obj(res)
        return obj

    async def __get_parent_id(self, children_id: UUID) -> Optional[UUID]:
        query = children.select().where(children.c.children_id == children_id)
        res = await self.database.fetch_one(query)
        if res is None:
            return None
        obj = Children.parse_obj(res)
        return obj.parent_id

    async def get_by_id(self, id: UUID) -> Optional[ShopUnit]:
        query = shop_unit.select().where(shop_unit.c.id == id)
        res = await self.database.fetch_one(query)
        if res is None:
            return None
        obj = ShopUnitDB.parse_obj(res)

        response = ShopUnit(
            id=obj.id,
            name=obj.name,
            date=obj.date,
            type=obj.shop_unit_type,
            price=obj.price if obj.shop_unit_type == "OFFER" else 0,
            parentId=await self.__get_parent_id(obj.id),
            children=await self.__get_children(obj.id),
        )
        tree = {**response.dict()}
        obj = ShopUnit.parse_obj(Price(tree).res())
        if obj.type == ShopUnitType.OFFER:
            obj.children = None
        return obj

    async def create(self, item: ShopUnitImport, date: datetime):
        new_shop_unit_item = ShopUnitDB(
            id=item.id,
            name=item.name,
            date=str(datetime.isoformat(date)),
            shop_unit_type=item.type,
            price=item.price
        )
        values = {**new_shop_unit_item.dict()}
        query = shop_unit.insert().values(**values)
        return await self.database.execute(query)

    async def update(self, item: ShopUnitImport, date: datetime) -> ShopUnitDB:
        update_shop_unit_item = ShopUnitDB(
            id=item.id,
            name=item.name,
            date=str(datetime.isoformat(date)),
            shop_unit_type=item.type,
            price=item.price
        )

        values = {**update_shop_unit_item.dict()}
        values.pop("id", None)
        query = shop_unit.update().where(shop_unit.c.id == item.id).values(**values)
        await self.database.execute(query=query)

        return update_shop_unit_item

    async def delete(self, id: UUID):
        query = children.select().where(children.c.parent_id == id)
        children_list = [Children.parse_obj(row) for row in await self.database.fetch_all(query)]
        if children_list:
            for child in children_list:
                await self.delete(child.children_id)
        query = shop_unit.delete().where(shop_unit.c.id == id)
        await self.database.execute(query=query)

        return "deleted"


class Price:
    def __init__(self, data):
        self.data = data
        self.sumList = []

    @staticmethod
    def mean_list(my_list: list):
        return sum(my_list) // len(my_list) if my_list else 0

    @staticmethod
    def merge_list(temp_list, branch_sum):
        res = []
        res += temp_list
        res += branch_sum
        return res

    def price(self, root, sum_list: list, branch_sum_list: list):
        branch_sum_list.clear()
        if root["children"]:
            for node in root["children"]:
                if node["type"] == "CATEGORY":
                    self.price(node, sum_list, branch_sum_list)

        temp_list = []
        for node in root["children"]:
            if node["type"] == "OFFER":
                sum_list.append(node["price"])
                temp_list.append(node["price"])

        root["price"] = self.mean_list(self.merge_list(temp_list, branch_sum_list))
        self.add_in_list_from_another_list(temp_list, branch_sum_list)

    @staticmethod
    def add_in_list_from_another_list(add_from: list, add_to: list):
        for i in add_from:
            add_to.append(i)

    def res(self):
        self.price(self.data, self.sumList, [])
        self.data["price"] = sum(self.sumList) // len(self.sumList)
        return self.data