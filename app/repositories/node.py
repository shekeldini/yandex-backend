from datetime import datetime
from typing import Optional
from uuid import UUID
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
            return await self.get_for_all_time(id)
        elif date_start and not date_end:
            return await self.get_for_start_time(id, date_start)
        else:
            return await self.get_for_interval(id, date_start, date_end)

    async def get_for_all_time(
            self,
            id: UUID
    ) -> ShopUnitStatisticResponse:
        query = """
        SELECT id, name, date, parent_id, price, type
        FROM statistic
        WHERE statistic.id = :id ORDER BY date;
        """
        values = {"id": id}
        res = await self.database.fetch_all(query=query, values=values)
        if not res:
            return ShopUnitStatisticResponse(
                items=[]
            )
        items = []
        for row in res:
            item = ShopUnitStatisticUnit.parse_obj(row)
            item.parentId = row[3]
            items.append(item)
        return ShopUnitStatisticResponse(
            items=items
        )

    async def get_for_start_time(
            self,
            id: UUID,
            date_start: datetime
    ) -> ShopUnitStatisticResponse:
        query = """
        SELECT id, name, date, parent_id, price, type
        FROM statistic
        WHERE statistic.id = :id
        AND statistic.date BETWEEN :date_start AND NOW()
        ORDER BY date;
        """
        values = {
            "id": id,
            "date_start": date_start.replace(tzinfo=None)
        }
        res = await self.database.fetch_all(query=query, values=values)
        if not res:
            return ShopUnitStatisticResponse(
                items=[]
            )
        items = []
        for row in res:
            item = ShopUnitStatisticUnit.parse_obj(row)
            item.parentId = row[3]
            items.append(item)
        return ShopUnitStatisticResponse(
            items=items
        )

    async def get_for_interval(
            self,
            id: UUID,
            date_start: datetime,
            date_end: datetime
    ) -> ShopUnitStatisticResponse:
        query = """
        SELECT id, name, date, parent_id, price, type
        FROM statistic
        WHERE statistic.id = :id
        AND statistic.date BETWEEN :date_start AND :date_end
        ORDER BY date;
        """
        values = {
            "id": id,
            "date_start": date_start.replace(tzinfo=None),
            "date_end": date_end.replace(tzinfo=None),
        }
        res = await self.database.fetch_all(query=query, values=values)
        if not res:
            return ShopUnitStatisticResponse(
                items=[]
            )
        items = []
        for row in res:
            item = ShopUnitStatisticUnit.parse_obj(row)
            item.parentId = row[3]
            items.append(item)
        return ShopUnitStatisticResponse(
            items=items
        )
