from uuid import UUID
from fastapi import APIRouter, Depends
from .depends import get_shop_unit_repository
from ..models.ShopUnit import ShopUnit
from ..repositories.shop_unit import ShopUnitRepository

router = APIRouter()


@router.delete("/{id}", response_model=str)
async def read_node_by_id(
        id: UUID,
        shop_unit_repository: ShopUnitRepository = Depends(get_shop_unit_repository)
):
    return await shop_unit_repository.delete(id)





