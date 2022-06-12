from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from .depends import get_shop_unit_repository, get_children_repository
from ..models.Children import Children
from ..models.ShopUnitImport import ShopUnitImport
from ..models.ShopUnitType import ShopUnitType
from ..repositories.children import ChildrenRepository
from ..repositories.shop_unit import ShopUnitRepository

router = APIRouter()


@router.get("/get_all", response_model=List[Children])
async def read_children(
        children: ChildrenRepository = Depends(get_children_repository)
):
    return await children.get_all()


@router.post("/")
async def create_children(
        import_shop_unit: ShopUnitImport,
        children_repository: ChildrenRepository = Depends(get_children_repository),
        shop_unit_repository: ShopUnitRepository = Depends(get_shop_unit_repository)
):

    parent = await shop_unit_repository.get_by_id(import_shop_unit.parentId)
    if parent.type != ShopUnitType.CATEGORY.value:
        raise ValueError("Parent type should be a category")
    return await children_repository.create(import_shop_unit)


@router.put("/")
async def update_children(
        import_shop_unit: ShopUnitImport,
        children_repository: ChildrenRepository = Depends(get_children_repository),
        shop_unit_repository: ShopUnitRepository = Depends(get_shop_unit_repository),
):
    parent = await shop_unit_repository.get_by_id(import_shop_unit.parentId)
    if parent.type != ShopUnitType.CATEGORY.value:
        raise ValueError("Parent type should be a category")
    return await children_repository.update(import_shop_unit)
