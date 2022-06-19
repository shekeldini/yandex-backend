from fastapi import APIRouter, Depends, Request
from .config.sales import RESPONSES, DESCRIPTION
from .depends import get_sales_repository
from ..core.config import INFO_KEY, INFO_MAX_REQUESTS, INFO_EXPIRE
from ..core.utils import remove_422, rate_limiter
from ..db.base import redis
from ..models.ShopUnitStatisticResponse import ShopUnitStatisticResponse
from ..models.sales import SalesDate
from ..repositories.sales import SalesRepository

router = APIRouter()


@router.get("",
            responses=RESPONSES,
            response_model=ShopUnitStatisticResponse,
            description=DESCRIPTION)
@remove_422
async def read_sales(
        request: Request,
        model: SalesDate = Depends(),
        sales_repository: SalesRepository = Depends(get_sales_repository)
):
    get_sales_func = rate_limiter(
        func=sales_repository.get_sales,
        redis=redis,
        key=INFO_KEY + request.client.host,
        limit=INFO_MAX_REQUESTS,
        period=INFO_EXPIRE
    )
    return await get_sales_func(model.date)
