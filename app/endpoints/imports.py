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
    parent_id_list = set()
    item_list = []
    for item in shop_unit_items.items:
        if item not in item_list:
            item_list.append(item)
        if item.parentId:
            parent_id_list.add(item.parentId)
        else:
            raise ValueError("Duplicate Id")

    for item in item_list:
        if await shop_unit_repository.get_by_id(item.id):
            await shop_unit_repository.update(item, date)
            await children_repository.update(item)
        else:
            await shop_unit_repository.create(item, date)
            await children_repository.create(item)

    for parent_id in parent_id_list:
        await shop_unit_repository.update_parent(parent_id, date)

    return
