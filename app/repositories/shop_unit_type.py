from typing import List, Optional
from ..models.ShopUnitType import ShopUnitTypeOutput
from ..db.shop_unit_type import shop_unit_type
from .base import BaseRepository


class ShopUnitTypeRepository(BaseRepository):
    async def get_all(self) -> List[ShopUnitTypeOutput]:
        query = shop_unit_type.select()
        return [ShopUnitTypeOutput.parse_obj(row) for row in await self.database.fetch_all(query)]

    async def create(self, input_shop_unit_type: ShopUnitTypeOutput):
        new_shop_unit_type = ShopUnitTypeOutput(
            shop_unit_type=input_shop_unit_type.shop_unit_type
        )
        values = {**new_shop_unit_type.dict()}
        query = shop_unit_type.insert().values(**values)
        return await self.database.execute(query)

    async def delete(self, input_shop_unit_type: ShopUnitTypeOutput):
        query = shop_unit_type.delete().where(shop_unit_type.c.shop_unit_type == input_shop_unit_type.shop_unit_type)

        return await self.database.execute(query=query)

