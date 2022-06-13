from uuid import UUID
from fastapi import APIRouter, Depends, status
from fastapi import HTTPException
from .depends import get_shop_unit_repository
from ..repositories.shop_unit import ShopUnitRepository

router = APIRouter()


@router.delete("/{id}", response_model=str)
async def read_node_by_id(
        id: UUID,
        shop_unit_repository: ShopUnitRepository = Depends(get_shop_unit_repository)
):
    if await shop_unit_repository.get_by_id(id):
        return await shop_unit_repository.delete(id)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")





