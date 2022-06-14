from uuid import UUID
from fastapi import APIRouter, Depends, status, Response, Body, Path, Query
from fastapi import HTTPException

from .config.delete import RESPONSES, DESCRIPTION
from .depends import get_shop_unit_repository
from ..core.utils import remove_422
from ..models.Error import Error
from ..models.delete import Delete
from ..repositories.shop_unit import ShopUnitRepository

router = APIRouter()


@router.delete("/{id}",
               responses=RESPONSES,
               response_class=Response,
               description=DESCRIPTION)
@remove_422
async def read_node_by_id(
        model: Delete = Depends(),
        shop_unit_repository: ShopUnitRepository = Depends(get_shop_unit_repository)
):
    if await shop_unit_repository.get_by_id(model.id):
        await shop_unit_repository.delete(model.id)
        return "Удаление прошло успешно."

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
