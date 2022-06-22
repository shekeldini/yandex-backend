from fastapi import APIRouter, Depends, HTTPException, status, Request
from .config.node import RESPONSES, DESCRIPTION
from .depends import get_node_repository, get_shop_unit_repository
from ..core.config import setting
from ..core.utils import remove_422, rate_limiter
from ..db.base import redis
from ..models.ShopUnitStatisticResponse import ShopUnitStatisticResponse
from ..models.StatisticRequest import StatisticRequest
from ..repositories.node import NodeRepository
from ..repositories.shop_unit import ShopUnitRepository

router = APIRouter()


@router.get("/{id}/statistic",
            responses=RESPONSES,
            response_model=ShopUnitStatisticResponse,
            description=DESCRIPTION)
@remove_422
async def get_statistic(
        request: Request,
        model: StatisticRequest = Depends(),
        node_repository: NodeRepository = Depends(get_node_repository),
        shop_unit_repository: ShopUnitRepository = Depends(get_shop_unit_repository)
):
    """
        Route /node/{id}/statistic with method 'get'

        For get statistic for shop unit item
    """
    # Try find existing item. If not existing we raise exception with status code 404
    if not await shop_unit_repository.get_by_id(model.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )
    # Wrapping the function node_repository.get_statistic for tracking rate limit for client ip
    get_statistic_func = rate_limiter(
        func=node_repository.get_statistic,
        redis=redis,
        key=setting.INFO_KEY + request.client.host,
        limit=setting.INFO_MAX_REQUESTS,
        period=setting.INFO_EXPIRE
    )
    # Call function to get statistic for item by id and date_start and date_end
    return await get_statistic_func(
        id=model.id,
        date_start=model.dateStart,
        date_end=model.dateEnd
    )
