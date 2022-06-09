from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app.repositories.shop_unit_type import ShopUnitTypeRepository
from app.models.ShopUnitType import ShopUnitType
from .depends import get_shop_unit_type_repository

router = APIRouter()


@router.get("/get_all", response_model=List[ShopUnitType])
async def read_shop_unit_type(
        shop_unit_type: ShopUnitTypeRepository = Depends(get_shop_unit_type_repository)
):
    return await shop_unit_type.get_all()


@router.post("/")
async def create_shop_unit_type(
        input_shop_unit_type: ShopUnitType,
        shop_unit_type: ShopUnitTypeRepository = Depends(get_shop_unit_type_repository)
):
    return await shop_unit_type.create(input_shop_unit_type)


@router.delete("/")
async def delete_district(
        input_shop_unit_type: ShopUnitType,
        shop_unit_type: ShopUnitTypeRepository = Depends(get_shop_unit_type_repository)
):
    return await shop_unit_type.delete(input_shop_unit_type)
