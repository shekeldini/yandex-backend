import pprint
from typing import List, Optional
from datetime import datetime
from uuid import UUID

from ..models.Children import Children
from ..models.ShopUnit import ShopUnit, ShopUnitDB
from ..db.shop_unit import shop_unit
from ..db.children import children
from .base import BaseRepository
from ..models.ShopUnitImport import ShopUnitImport
from ..models.ShopUnitType import ShopUnitType


class ShopUnitRepository(BaseRepository):
    async def get_children(self, id: UUID):
        res = []

        async def get(id, res):
            query = children.select().where(children.c.parent_id == id)
            children_list = [Children.parse_obj(row) for row in await self.database.fetch_all(query)]
            if children_list:
                for item in children_list:

                    children_obj = ShopUnitDB.parse_obj(await self.get_by_id_from_db(item.children_id))
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

    async def get_by_id_from_db(self, id: UUID) -> Optional[ShopUnitDB]:
        query = shop_unit.select().where(shop_unit.c.id == id)
        res = await self.database.fetch_one(query)
        if res is None:
            return None
        obj = ShopUnitDB.parse_obj(res)
        return obj

    async def get_parent_id(self, children_id: UUID) -> Optional[UUID]:
        query = children.select().where(children.c.children_id == children_id)
        res = await self.database.fetch_one(query)
        if res is None:
            return None
        obj = Children.parse_obj(res)
        return obj.parent_id

    async def get_by_id(self, id: UUID) -> Optional[ShopUnit]:
        def sum_price(root: list, x=0, c=0):
            for node in root:
                if node["type"] == "CATEGORY":
                    node["price"] = sum_price(node["children"])
                else:
                    x += node["price"]
                    c += 1

            return x // c if c else x

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
            parentId=await self.get_parent_id(obj.id),
            children=await self.get_children(obj.id),
        )
        tree = {**response.dict()}
        sum_price(tree["children"])
        for i in tree["children"]:
            tree["price"] += i["price"] // len(tree["children"])
        return ShopUnit.parse_obj(tree)

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

    async def delete(self, id: UUID):
        query = shop_unit.delete().where(shop_unit.c.id == id)
        return await self.database.execute(query=query)

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
