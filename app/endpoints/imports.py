from fastapi import APIRouter, Depends, HTTPException, status
from .depends import get_shop_unit_repository
from ..models.ShopUnitImportRequest import ShopUnitImportRequest
from ..repositories.shop_unit import ShopUnitRepository

router = APIRouter()


@router.post("/")
async def create_shop_unit_type(
        shop_unit_items: ShopUnitImportRequest,
        shop_unit_repository: ShopUnitRepository = Depends(get_shop_unit_repository)
):
    date = shop_unit_items.updateDate
    for item in shop_unit_items.items:
        if await shop_unit_repository.get_by_id(item.id):
            await shop_unit_repository.update(item, date)
        else:
            await shop_unit_repository.create(item, date)
    return
