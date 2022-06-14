from fastapi import APIRouter, Depends, Response

from .config.imports import RESPONSES, DESCRIPTION
from .depends import get_shop_unit_repository, get_children_repository
from ..core.utils import remove_422
from ..models.ShopUnitImportRequest import ShopUnitImportRequest
from ..repositories.shop_unit import ShopUnitRepository
from ..repositories.children import ChildrenRepository

router = APIRouter()


@router.post("",
             responses=RESPONSES,
             response_class=Response,
             description=DESCRIPTION)
@remove_422
async def create_shop_unit_type(
        shop_unit_items: ShopUnitImportRequest,
        shop_unit_repository: ShopUnitRepository = Depends(get_shop_unit_repository),
        children_repository: ChildrenRepository = Depends(get_children_repository),
):
    date = shop_unit_items.updateDate
    parent_id_list = set()
    for item in shop_unit_items.items:
        if await shop_unit_repository.get_by_id(item.id):
            await shop_unit_repository.update(item, date)
            await children_repository.update(item)
        else:
            await shop_unit_repository.create(item, date)
            await children_repository.create(item)

        if item.parentId:
            parent_id_list.add(item.parentId)

    for parent_id in parent_id_list:
        await shop_unit_repository.update_parent(parent_id, date)

    return
