from datetime import datetime, timedelta

from dateutil import parser

from .base import BaseRepository
from ..models.ShopUnitStatisticResponse import ShopUnitStatisticResponse
from ..models.ShopUnitStatisticUnit import ShopUnitStatisticUnit


class SalesRepository(BaseRepository):
    async def get_sales(self, date: str) -> ShopUnitStatisticResponse:
        query = """
        SELECT id, name, date, type, price, parent_id
        FROM shop_unit
        LEFT JOIN childrens ON shop_unit.id=childrens.children_id
        WHERE shop_unit.date BETWEEN :first_date AND :second_date
        AND shop_unit.type = 'OFFER';
        """


        values = {
            "first_date": date,
            "second_date": (
                    datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.000Z") + timedelta(hours=24)
            ).strftime("%Y-%m-%dT%H:%M:%S.000Z")
        }
        res = await self.database.fetch_all(query, values)
        if not res:
            return ShopUnitStatisticResponse(items=[])
        return ShopUnitStatisticResponse(items=[ShopUnitStatisticUnit.parse_obj(row) for row in res])
