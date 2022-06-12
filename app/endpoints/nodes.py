from uuid import UUID
from fastapi import APIRouter, Depends
from .depends import get_shop_unit_repository
from ..models.ShopUnit import ShopUnit
from ..repositories.shop_unit import ShopUnitRepository

router = APIRouter()


@router.get("/{id}", response_model=ShopUnit)
async def read_node_by_id(
        id: UUID,
        shop_unit_repository: ShopUnitRepository = Depends(get_shop_unit_repository)
):
    return await shop_unit_repository.get_by_id(id)





