from fastapi import APIRouter, Depends
from .config.sales import RESPONSES, DESCRIPTION
from .depends import get_sales_repository
from ..core.utils import remove_422
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
        model: SalesDate = Depends(),
        sales_repository: SalesRepository = Depends(get_sales_repository)
):
    """
        Route /sales with method 'get'

        Get information about OFFERS for 24h from start date
    """
    # Get sales information
    return await sales_repository.get_sales(model.date)
