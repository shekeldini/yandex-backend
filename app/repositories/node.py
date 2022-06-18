from datetime import datetime
from typing import Optional
from uuid import UUID
from .children import ChildrenRepository
from .base import BaseRepository
from ..models.ShopUnitStatisticResponse import ShopUnitStatisticResponse
from ..models.ShopUnitStatisticUnit import ShopUnitStatisticUnit


class NodeRepository(BaseRepository):
    async def get_statistic(
            self,
            id: UUID,
            date_start: Optional[datetime],
            date_end: Optional[datetime]
    ) -> ShopUnitStatisticResponse:
        if not (date_start or date_end):
            return await self.get_all_time(id)

    async def get_all_time(
            self,
            id: UUID
    ) -> ShopUnitStatisticResponse:
        query = """
        SELECT id, name, date, type, price, parent_id
        FROM statistic
        LEFT JOIN childrens ON shop_unit.id=childrens.children_id
        WHERE shop_unit.id = :id;
        """
        values = {"id": id}

        return ShopUnitStatisticResponse(
            items=[
                ShopUnitStatisticUnit.parse_obj(row) for row in await self.database.fetch_all(
                    query=query, values=values
                )
            ]
        )
