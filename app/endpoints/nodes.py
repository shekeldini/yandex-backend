from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from .depends import get_nodes_repository, get_shop_unit_repository
from ..core.utils import remove_422
from ..models.Error import Error
from ..models.ShopUnit import ShopUnit
from ..repositories.nodes import NodesRepository
from ..repositories.shop_unit import ShopUnitRepository


router = APIRouter()
responses = {
    200: {
        "description": "Удаление прошло успешно.",
    },
    400: {
        "model": Error,
        "description": "Невалидная схема документа или входные данные не верны.",
        "content": {
            "application/json": {
                "examples": {
                    "response": {
                        "value": {
                            "code": 400,
                            "message": "Validation Failed"
                        }
                    }
                }
            }
        }
    },
    404: {
        "model": Error,
        "description": "Категория/товар не найден.",
        "content": {
            "application/json": {
                "examples": {
                    "response": {
                        "value": {
                            "code": 404,
                            "message": "Item not found"
                        }
                    }
                }
            }
        }
    }
}
description = """Получить информацию об элементе по идентификатору. 
При получении информации о категории также предоставляется информация о её дочерних элементах.

- цена категории - это средняя цена всех её товаров, включая товары дочерних категорий.
Если категория не содержит товаров цена равна null.
При обновлении цены товара, средняя цена категории, которая содержит этот товар, тоже обновляется."""


@router.get("/{id}", responses=responses, response_model=ShopUnit, description=description)
@remove_422
async def read_node_by_id(
        id: UUID,
        nodes_repository: NodesRepository = Depends(get_nodes_repository),
        shop_unit_repository: ShopUnitRepository = Depends(get_shop_unit_repository),
):
    if await shop_unit_repository.get_by_id(id):
        return await nodes_repository.get_by_id(id)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")





