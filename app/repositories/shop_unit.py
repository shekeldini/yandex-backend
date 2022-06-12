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
    async def get_all(self) -> List[ShopUnit]:

        query = shop_unit.select()
        res = []
        # for row in await self.database.fetch_all(query):
        #     item = ShopUnitDB.parse_obj(row)
        #     if item.shop_unit_type == ShopUnitType.CATEGORY.value:
        #         await self.get_children(item.id)
        return res

    async def get_children(self, id: UUID):
        res = {}

        async def get(id, res):
            query = children.select().where(children.c.parent_id == id)
            children_list = [Children.parse_obj(row) for row in await self.database.fetch_all(query)]
            if children_list:
                res["children"] = []
                for item in children_list:
                    children_obj = ShopUnitDB.parse_obj(await self.get_by_id(item.children_id))

                    res["id"] = children_obj.id
                    res["shop_unit_type"] = children_obj.shop_unit_type
                    res["price"] = children_obj.price
                    res["name"] = children_obj.name
                    res["date"] = children_obj.date
                    res["children"].append({})

                    if children_obj.shop_unit_type == ShopUnitType.CATEGORY.value:
                        await get(children_obj.id, res["children"][-1])
        await get(id, res)
        return res

    async def get_by_id(self, id: UUID) -> Optional[ShopUnitDB]:
        query = shop_unit.select().where(shop_unit.c.id == id)
        res = await self.database.fetch_one(query)
        if res is None:
            return None
        obj = ShopUnitDB.parse_obj(res)
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


