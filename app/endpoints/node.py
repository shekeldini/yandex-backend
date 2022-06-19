from fastapi import APIRouter, Depends, HTTPException, status, Request
from .config.node import RESPONSES, DESCRIPTION
from .depends import get_node_repository, get_shop_unit_repository
from ..core.config import INFO_KEY, INFO_MAX_REQUESTS, INFO_EXPIRE
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
    if not await shop_unit_repository.get_by_id(model.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"
        )

    get_statistic_func = rate_limiter(
        func=node_repository.get_statistic,
        redis=redis,
        key=INFO_KEY + request.client.host,
        limit=INFO_MAX_REQUESTS,
        period=INFO_EXPIRE
    )
    return await get_statistic_func(
        id=model.id,
        date_start=model.dateStart,
        date_end=model.dateEnd
    )
