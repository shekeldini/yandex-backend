from fastapi import APIRouter, Depends, HTTPException, status, Request
from .config.nodes import RESPONSES, DESCRIPTION
from .depends import get_nodes_repository, get_shop_unit_repository
from ..core.config import setting
from ..core.utils import remove_422, rate_limiter
from ..db.base import redis
from ..models.ShopUnit import ShopUnit
from ..models.nodes import Nodes
from ..repositories.nodes import NodesRepository
from ..repositories.shop_unit import ShopUnitRepository

router = APIRouter()


@router.get("/{id}",
            responses=RESPONSES,
            response_model=ShopUnit,
            description=DESCRIPTION)
@remove_422
async def read_node_by_id(
        request: Request,
        model: Nodes = Depends(),
        nodes_repository: NodesRepository = Depends(get_nodes_repository),
        shop_unit_repository: ShopUnitRepository = Depends(get_shop_unit_repository),
):
    """
        Route /nodes/{id} with method 'get'

        Get all information for shop unit item
    """
    # Try find existing item. If not existing we raise exception with status code 404
    if await shop_unit_repository.get_by_id(model.id):
        # Wrapping the function nodes_repository.get_by_id for tracking rate limit for client ip
        get_node_func = rate_limiter(
            func=nodes_repository.get_by_id,
            redis=redis,
            key=setting.INFO_KEY + request.client.host,
            limit=setting.INFO_MAX_REQUESTS,
            period=setting.INFO_EXPIRE
        )
        return await get_node_func(model.id)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
