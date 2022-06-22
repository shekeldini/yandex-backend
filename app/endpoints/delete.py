from fastapi import APIRouter, Depends, status, Response, Request
from fastapi import HTTPException
from .config.delete import RESPONSES, DESCRIPTION
from .depends import get_shop_unit_repository
from ..core.config import setting
from ..core.utils import remove_422, rate_limiter
from ..db.base import redis
from ..models.delete import DeleteId
from ..repositories.shop_unit import ShopUnitRepository

router = APIRouter()


@router.delete("/{id}",
               responses=RESPONSES,
               response_class=Response,
               description=DESCRIPTION)
@remove_422
async def delete(
        request: Request,
        model: DeleteId = Depends(),
        shop_unit_repository: ShopUnitRepository = Depends(get_shop_unit_repository)
):
    """
    Route /delete/{id} with method 'delete'
    """
    # Try find existing item. If not found raise 404 exception
    if await shop_unit_repository.get_by_id(model.id):
        # Wrapping the function shop_unit_repository.delete for tracking rate limit for client ip
        delete_func = rate_limiter(
            func=shop_unit_repository.delete,
            redis=redis,
            key=setting.DELETE_KEY + request.client.host,
            limit=setting.DELETE_MAX_REQUESTS,
            period=setting.DELETE_EXPIRE
        )
        # Call function for delete item by id and delete all children
        return await delete_func(model.id)
    # Raise 404 exception if item not found
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
