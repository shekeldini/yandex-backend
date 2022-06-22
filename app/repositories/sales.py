from datetime import datetime, timedelta
from .base import BaseRepository
from ..models.ShopUnitStatisticResponse import ShopUnitStatisticResponse
from ..models.ShopUnitStatisticUnit import ShopUnitStatisticUnit


class SalesRepository(BaseRepository):
    """
        A class SalesRepository for get sales

        Methods
            -get_sales(date: datetime)
                return OFFERS where OFFER.date BETWEEN date AND date + 24h
        """
    async def get_sales(self, date: datetime) -> ShopUnitStatisticResponse:
        """return OFFERS where OFFER.date BETWEEN date AND date + 24h"""
        query = """
        SELECT id, name, parent_id, date, type, price 
        FROM shop_unit
        LEFT JOIN childrens ON shop_unit.id=childrens.children_id
        WHERE shop_unit.date BETWEEN :first_date AND :second_date
        AND shop_unit.type = 'OFFER';
        """

        values = {
            "first_date": date.replace(tzinfo=None),
            "second_date": (
                (date + timedelta(hours=24)).replace(tzinfo=None)
            )
        }
        res = await self.database.fetch_all(query, values)
        if not res:
            # if res for first_date and second_date is empty return empty items list
            return ShopUnitStatisticResponse(items=[])

        items = []
        for row in res:
            item = ShopUnitStatisticUnit.parse_obj(row)
            item.parentId = row.parent_id
            items.append(item)
        return ShopUnitStatisticResponse(
            items=items
        )
