from fastapi import APIRouter, Depends, status, Response
from fastapi import HTTPException
from .config.delete import RESPONSES, DESCRIPTION
from .depends import get_shop_unit_repository
from ..core.utils import remove_422
from ..models.delete import DeleteId
from ..repositories.shop_unit import ShopUnitRepository

router = APIRouter()


@router.delete("/{id}",
               responses=RESPONSES,
               response_class=Response,
               description=DESCRIPTION)
@remove_422
async def delete(
        model: DeleteId = Depends(),
        shop_unit_repository: ShopUnitRepository = Depends(get_shop_unit_repository)
):
    """
    Route /delete/{id} with method 'delete'
    """
    # Try find existing item. If not found raise 404 exception
    if await shop_unit_repository.get_by_id(model.id):
        # Call function for delete item by id and delete all children
        return await shop_unit_repository.delete(model.id)
    # Raise 404 exception if item not found
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
