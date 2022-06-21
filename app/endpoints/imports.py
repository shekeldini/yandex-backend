from fastapi import APIRouter, Depends, Response, Request
from .config.imports import RESPONSES, DESCRIPTION
from .depends import get_shop_unit_repository, get_children_repository
from ..core.config import IMPORT_KEY, IMPORT_MAX_REQUESTS, IMPORT_EXPIRE
from ..core.utils import remove_422, request_is_limited, TooManyRequests, CanNotChangeType
from ..db.base import redis
from ..models.ShopUnitImportRequest import ShopUnitImportRequest
from ..models.ShopUnitType import ShopUnitType
from ..repositories.children import ChildrenRepository
from ..repositories.shop_unit import ShopUnitRepository

router = APIRouter()


@router.post("",
             responses=RESPONSES,
             response_class=Response,
             description=DESCRIPTION)
@remove_422
async def import_shop_unit(
        shop_unit_items: ShopUnitImportRequest,
        request: Request,
        shop_unit_repository: ShopUnitRepository = Depends(get_shop_unit_repository),
        children_repository: ChildrenRepository = Depends(get_children_repository)
):
    date = shop_unit_items.updateDate
    need_update = {
        "price": [],
        "date": []
    }
    limited = False
    for item in shop_unit_items.items:
        if not request_is_limited(
                r=redis,
                key=IMPORT_KEY + request.client.host,
                limit=IMPORT_MAX_REQUESTS,
                period=IMPORT_EXPIRE
        ):
            exist_item = await shop_unit_repository.get_by_id(item.id)
            if exist_item:
                if exist_item.type != item.type:
                    raise CanNotChangeType()
                await shop_unit_repository.update(item, date)
            else:
                await shop_unit_repository.create(item, date)

            if item.parentId and item.type == ShopUnitType.OFFER.value and item.parentId not in need_update["price"]:
                need_update["price"].append(item.parentId)

            if item.parentId and item.parentId not in need_update["date"]:
                need_update["date"].append(item.parentId)
        else:
            limited = True
            break
    price_updated = set()
    date_updated = set()

    for parentId in need_update["price"]:
        root_parent_id = await children_repository.get_root_category_id(parentId)
        if root_parent_id not in price_updated:
            await shop_unit_repository.update_parent_price(parentId)
            price_updated.add(root_parent_id)

    for parentId in need_update["date"]:
        if parentId not in date_updated:
            all_parents = await shop_unit_repository.get_all_parents_for_parent(parentId, [])
            for id in all_parents:
                if id not in date_updated:
                    await shop_unit_repository.update_date(id, date)
                    date_updated.add(id)
    if limited:
        raise TooManyRequests()
    return
