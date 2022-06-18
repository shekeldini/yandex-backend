from datetime import datetime, timedelta
from .base import BaseRepository
from ..core.config import DATE_TIME_FORMAT
from ..models.ShopUnitStatisticResponse import ShopUnitStatisticResponse
from ..models.ShopUnitStatisticUnit import ShopUnitStatisticUnit


class SalesRepository(BaseRepository):
    async def get_sales(self, date: datetime) -> ShopUnitStatisticResponse:
        query = """
        SELECT id, name, date, type, price, parent_id
        FROM shop_unit
        LEFT JOIN childrens ON shop_unit.id=childrens.children_id
        WHERE shop_unit.date BETWEEN :first_date AND :second_date
        AND shop_unit.type = 'OFFER';
        """


        values = {
            "first_date": date.strftime(DATE_TIME_FORMAT),
            "second_date": (
                    date + timedelta(hours=24)
            ).strftime(DATE_TIME_FORMAT)
        }
        res = await self.database.fetch_all(query, values)
        if not res:
            return ShopUnitStatisticResponse(items=[])
        return ShopUnitStatisticResponse(items=[ShopUnitStatisticUnit.parse_obj(row) for row in res])
