from typing import Optional
from uuid import UUID
from ..db.children import children
from ..models.Children import Children
from ..models.ShopUnit import ShopUnitDB
from ..db.shop_unit import shop_unit
from .base import BaseRepository
from ..models.ShopUnitImport import ShopUnitImport


class ShopUnitRepository(BaseRepository):
    async def get_by_id(self, id: UUID) -> Optional[ShopUnitDB]:
        query = shop_unit.select().where(shop_unit.c.id == id)
        res = await self.database.fetch_one(query)
        if res is None:
            return None
        return ShopUnitDB.parse_obj(res)

    async def update_parent(self, child_id: UUID, date: str):
        print("func update_parent child_id=", child_id)
        query = children.select().where(children.c.children_id == child_id)
        res = await self.database.fetch_one(query)
        if res:
            child = Children.parse_obj(res)
            print("func update_parent parent_id=", child.parent_id)
            await self.update_parent(child.parent_id, date)
        print("no parent")
        item = await self.get_by_id(child_id)
        print("update data id=", item.id)
        print()
        return await self.update_date(item, date)

    async def update_date(self, item: ShopUnitDB, date: str):

        update_data = ShopUnitDB(
            id=item.id,
            name=item.name,
            date=date,
            shop_unit_type=item.shop_unit_type,
            price=item.price
        )
        values = {**update_data.dict()}
        values.pop("id", None)
        query = shop_unit.update().where(shop_unit.c.id == update_data.id).values(**values)
        await self.database.execute(query=query)
        return "updated"

    async def create(self, item: ShopUnitImport, date: str):

        new_shop_unit_item = ShopUnitDB(
            id=item.id,
            name=item.name,
            date=date,
            shop_unit_type=item.type,
            price=item.price
        )
        values = {**new_shop_unit_item.dict()}
        query = shop_unit.insert().values(**values)
        return await self.database.execute(query)



    async def update(self, item: ShopUnitImport, date: str) -> ShopUnitDB:
        update_shop_unit_item = ShopUnitDB(
            id=item.id,
            name=item.name,
            date=date,
            shop_unit_type=item.type,
            price=item.price
        )

        values = {**update_shop_unit_item.dict()}
        values.pop("id", None)
        query = shop_unit.update().where(shop_unit.c.id == update_shop_unit_item.id).values(**values)
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
