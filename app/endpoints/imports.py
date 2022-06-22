from fastapi import APIRouter, Depends, Response, Request
from .config.imports import RESPONSES, DESCRIPTION
from .depends import get_shop_unit_repository, get_children_repository
from ..core.config import setting
from ..core.utils import remove_422, request_is_limited
from app.core.exception import TooManyRequests, CanNotChangeType
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
    """
        Route /import with method 'post'
    """
    # UpdateDate from request
    date = shop_unit_items.updateDate

    # Here stored items which after create/update should update date or price parent
    need_update = {
        "price": [],
        "date": []
    }
    # Limited flag
    limited = False
    for item in shop_unit_items.items:
        # Check request limit is exceeded for client ip
        if not request_is_limited(
                r=redis,
                key=setting.IMPORT_KEY + request.client.host,
                limit=setting.IMPORT_MAX_REQUESTS,
                period=setting.IMPORT_EXPIRE
        ):
            # Try find existing item.
            exist_item = await shop_unit_repository.get_by_id(item.id)

            if exist_item:
                # If item existing and their categories don't match raise CanNotChangeType exception
                if exist_item.type != item.type:
                    raise CanNotChangeType()
                # Update existing item
                await shop_unit_repository.update(item, date)
            else:
                # Create new item
                await shop_unit_repository.create(item, date)

            # If item have parentId and item.type is OFFER we should update parent price
            if item.parentId and item.type == ShopUnitType.OFFER.value and item.parentId not in need_update["price"]:
                need_update["price"].append(item.parentId)
            # If item have parentId we should update parent date
            if item.parentId and item.parentId not in need_update["date"]:
                need_update["date"].append(item.parentId)
        else:
            limited = True
            # stop update/create item
            break
    # Storage all parentId who has been updated for not to update twice
    price_updated = set()
    date_updated = set()

    for parentId in need_update["price"]:
        # We should update all parent price so we find the root parent id
        root_parent_id = await children_repository.get_root_category_id(parentId)
        # If we didn't update root parent id we should do it
        if root_parent_id not in price_updated:
            # Update root parent price and all children category price
            await shop_unit_repository.update_parent_price(parentId)
            # Add root parent id to storage
            price_updated.add(root_parent_id)

    for parentId in need_update["date"]:
        # If we didn't update root parent id we should do it
        if parentId not in date_updated:
            # We should update all parent date so we find all items who need update date
            all_parents = await shop_unit_repository.get_all_parents_for_parent(parentId, [])
            for id in all_parents:
                if id not in date_updated:
                    # Update parent date for parent
                    await shop_unit_repository.update_date(id, date)
                    # Add parent id to storage
                    date_updated.add(id)
    # If limited flag True we raise TooManyRequests exception
    if limited:
        raise TooManyRequests()
    return
