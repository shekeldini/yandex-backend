from fastapi import APIRouter, Depends, HTTPException, status
from ..repositories.shop_unit_import_request import ShopUnitImportRequestRepository
from .depends import get_shop_unit_import_request_repository
from ..models.ShopUnitImportRequest import ShopUnitImportRequest

router = APIRouter()


@router.post("/")
async def create_shop_unit_type(
        shop_unit_items: ShopUnitImportRequest,
        shop_unit_import_request: ShopUnitImportRequestRepository = Depends(get_shop_unit_import_request_repository)
):
    return await shop_unit_import_request.create(shop_unit_items)
