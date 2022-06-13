from uuid import UUID
from fastapi import APIRouter, Depends
from .depends import get_nodes_repository
from ..models.ShopUnit import ShopUnit
from ..repositories.nodes import NodesRepository

router = APIRouter()


@router.get("/{id}", response_model=ShopUnit)
async def read_node_by_id(
        id: UUID,
        shop_unit_repository: NodesRepository = Depends(get_nodes_repository)
):
    return await shop_unit_repository.get_by_id(id)





