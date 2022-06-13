from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from .depends import get_nodes_repository, get_shop_unit_repository
from ..models.ShopUnit import ShopUnit
from ..repositories.nodes import NodesRepository
from ..repositories.shop_unit import ShopUnitRepository


router = APIRouter()


@router.get("/{id}", response_model=ShopUnit)
async def read_node_by_id(
        id: UUID,
        nodes_repository: NodesRepository = Depends(get_nodes_repository),
        shop_unit_repository: ShopUnitRepository = Depends(get_shop_unit_repository),
):
    if await shop_unit_repository.get_by_id(id):
        return await nodes_repository.get_by_id(id)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")





