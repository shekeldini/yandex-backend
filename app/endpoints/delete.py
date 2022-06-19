from fastapi import APIRouter, Depends, status, Response, Request
from fastapi import HTTPException
from .config.delete import RESPONSES, DESCRIPTION
from .depends import get_shop_unit_repository
from ..core.config import DELETE_KEY, DELETE_MAX_REQUESTS, DELETE_EXPIRE
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
    if await shop_unit_repository.get_by_id(model.id):
        delete_func = rate_limiter(
            func=shop_unit_repository.delete,
            redis=redis,
            key=DELETE_KEY + request.client.host,
            limit=DELETE_MAX_REQUESTS,
            period=DELETE_EXPIRE
        )
        return await delete_func(model.id)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
