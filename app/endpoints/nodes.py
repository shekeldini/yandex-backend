from fastapi import APIRouter, Depends, HTTPException, status, Request
from .config.nodes import RESPONSES, DESCRIPTION
from .depends import get_nodes_repository, get_shop_unit_repository
from ..core.config import INFO_KEY, INFO_MAX_REQUESTS, INFO_EXPIRE
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
    if await shop_unit_repository.get_by_id(model.id):
        get_node_func = rate_limiter(
            func=nodes_repository.get_by_id,
            redis=redis,
            key=INFO_KEY + request.client.host,
            limit=INFO_MAX_REQUESTS,
            period=INFO_EXPIRE
        )
        return await get_node_func(model.id)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
