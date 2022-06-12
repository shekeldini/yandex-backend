import pprint
from datetime import datetime
from typing import List
from uuid import UUID
from dateutil import parser

from fastapi import APIRouter, Depends, HTTPException, status
from app.models.ShopUnitType import ShopUnitTypeOutput
from .depends import get_shop_unit_repository, get_children_repository
from ..models.ShopUnit import ShopUnit, ShopUnitDB
from ..models.ShopUnitImport import ShopUnitImport
from ..repositories.children import ChildrenRepository
from ..repositories.shop_unit import ShopUnitRepository

router = APIRouter()


@router.get("/get_all", response_model=List[ShopUnit])
async def read_shop_unit(
        shop_type: ShopUnitRepository = Depends(get_shop_unit_repository)
):
    return await shop_type.get_all()


@router.get("/get_by_id", response_model=ShopUnitDB)
async def read_shop_unit_by_id(
        id: UUID,
        shop_type: ShopUnitRepository = Depends(get_shop_unit_repository)

):
    pprint.pprint(await shop_type.get_children("069cb8d7-bbdd-47d3-ad8f-82ef4c269df1"))
    return await shop_type.get_by_id(id)


@router.post("/")
async def create_shop_unit(
        import_shop_unit: ShopUnitImport,
        date: datetime,
        shop_unit: ShopUnitRepository = Depends(get_shop_unit_repository),
        children_repository: ChildrenRepository = Depends(get_children_repository)
):
    await shop_unit.create(import_shop_unit, date)
    if import_shop_unit.parentId:
        await children_repository.create(import_shop_unit)
    return 200


@router.put("/")
async def update_shop_unit(
        import_shop_unit: ShopUnitImport,
        date: datetime,
        shop_unit_repository: ShopUnitRepository = Depends(get_shop_unit_repository),
        children_repository: ChildrenRepository = Depends(get_children_repository)
):
    exist_shop_unit_item = await shop_unit_repository.get_by_id(import_shop_unit.id)
    if exist_shop_unit_item.type != import_shop_unit.type:
        raise ValueError("Incorrect update item type")
    await shop_unit_repository.update(import_shop_unit, date)

    if import_shop_unit.parentId:
        await children_repository.update(import_shop_unit)

    return 200


@router.delete("/")
async def delete_district(
        id: UUID,
        shop_unit_type: ShopUnitRepository = Depends(get_shop_unit_repository)
):
    return await shop_unit_type.delete(id)
