from fastapi import APIRouter, Depends, HTTPException, status
from .depends import get_shop_unit_repository, get_children_repository
from ..models.ShopUnitImportRequest import ShopUnitImportRequest
from ..repositories.shop_unit import ShopUnitRepository
from ..repositories.children import ChildrenRepository

router = APIRouter()


@router.post("")
async def create_shop_unit_type(
        shop_unit_items: ShopUnitImportRequest,
        shop_unit_repository: ShopUnitRepository = Depends(get_shop_unit_repository),
        children_repository: ChildrenRepository = Depends(get_children_repository),
):
    date = shop_unit_items.updateDate
    for item in shop_unit_items.items:
        if await shop_unit_repository.get_by_id(item.id):
            await shop_unit_repository.update(item, date)
            await children_repository.update(item)
        else:
            await shop_unit_repository.create(item, date)
            await children_repository.create(item)
        if item.parentId:
            await shop_unit_repository.update_parent(item.id, date)

    return
