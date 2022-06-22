from datetime import datetime
from typing import Optional
from uuid import UUID
from .base import BaseRepository
from ..models.ShopUnitStatisticResponse import ShopUnitStatisticResponse
from ..models.ShopUnitStatisticUnit import ShopUnitStatisticUnit


class NodeRepository(BaseRepository):
    """
    Class NodeRepository return statistic for shop unit item by id and date_start and date_end
        Methods
            -get_statistic(id: UUID, date_start: Optional[datetime], date_end: Optional[datetime])
                Controller
            -get_for_all_time(id: UUID)
                return statistic for all time
            -get_for_start_time(id: UUID, date_start: datetime)
                return statistic for date BETWEEN date_start AND NOW()
            -get_for_interval(id: UUID, date_start: datetime, date_end: datetime)
                return statistic for date BETWEEN date_start AND date_end
    """
    async def get_statistic(
            self,
            id: UUID,
            date_start: Optional[datetime],
            date_end: Optional[datetime]
    ) -> ShopUnitStatisticResponse:
        """Controller: calls functions depending on the passed parameters"""
        if not (date_start or date_end):
            # if date_start is None and date_end is None -> get statistic for all time
            return await self.get_for_all_time(id)
        elif date_start and not date_end:
            # if only date_start -> get statistic for date BETWEEN date_start AND NOW()
            return await self.get_for_start_time(id, date_start)
        else:
            # if date_start and date_end -> get statistic for date BETWEEN date_start AND date_end
            return await self.get_for_interval(id, date_start, date_end)

    async def get_for_all_time(
            self,
            id: UUID
    ) -> ShopUnitStatisticResponse:
        """get statistic for all time for id shop unit item"""
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
            item.parentId = row.parent_id
            items.append(item)
        return ShopUnitStatisticResponse(
            items=items
        )

    async def get_for_start_time(
            self,
            id: UUID,
            date_start: datetime
    ) -> ShopUnitStatisticResponse:
        """Get statistic for date BETWEEN date_start AND NOW() by shop unit id"""
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
            item.parentId = row.parent_id
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
        """get statistic for date BETWEEN date_start AND date_end by shop unit item id"""
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
            item.parentId = row.parent_id
            items.append(item)
        return ShopUnitStatisticResponse(
            items=items
        )
