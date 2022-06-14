from uuid import UUID
from fastapi import APIRouter, Depends, status, Response, Body, Path, Query
from fastapi import HTTPException
from .depends import get_shop_unit_repository
from ..core.utils import remove_422
from ..models.Error import Error
from ..models.delete import Delete
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
description = """Удалить элемент по идентификатору. При удалении категории удаляются все дочерние элементы. 
Доступ к статистике (истории обновлений) удаленного элемента невозможен.

**Обратите, пожалуйста, внимание на этот обработчик. При его некорректной работе тестирование может быть невозможно.**"""


@router.delete("/{id}", responses=responses, response_class=Response, description=description)
@remove_422
async def read_node_by_id(
        model: Delete,
        shop_unit_repository: ShopUnitRepository = Depends(get_shop_unit_repository)
):
    if await shop_unit_repository.get_by_id(model.id):
        await shop_unit_repository.delete(model.id)
        return "Удаление прошло успешно."

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
