from fastapi import APIRouter, Depends, Response
from .config.imports import RESPONSES, DESCRIPTION
from .depends import get_shop_unit_repository
from ..core.utils import remove_422
from ..models.ShopUnitImportRequest import ShopUnitImportRequest
from ..models.ShopUnitType import ShopUnitType
from ..repositories.shop_unit import ShopUnitRepository

router = APIRouter()


@router.post("",
             responses=RESPONSES,
             response_class=Response,
             description=DESCRIPTION)
@remove_422
async def create_shop_unit_type(
        shop_unit_items: ShopUnitImportRequest,
        shop_unit_repository: ShopUnitRepository = Depends(get_shop_unit_repository)
):
    date = shop_unit_items.updateDate
    parent_id_list = []
    for item in shop_unit_items.items:
        if await shop_unit_repository.get_by_id(item.id):
            await shop_unit_repository.update(item, date)
        else:
            await shop_unit_repository.create(item, date)

        if item.parentId and item not in parent_id_list:
            parent_id_list.append(item)

    for item in parent_id_list:
        await shop_unit_repository.update_parent_date(item.parentId, date)
        if item.type == ShopUnitType.OFFER.value:
            await shop_unit_repository.update_parent_price(item.parentId)
    return
