from fastapi import APIRouter, Depends, HTTPException, status, Response
from .depends import get_shop_unit_repository, get_children_repository
from ..core.utils import remove_422
from ..models.Error import Error
from ..models.ShopUnitImportRequest import ShopUnitImportRequest
from ..repositories.shop_unit import ShopUnitRepository
from ..repositories.children import ChildrenRepository

router = APIRouter()
responses = {
    200: {
        "description": "Вставка или обновление прошли успешно.",
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
    422: {}
}
description = """Импортирует новые товары и/или категории.
Товары/категории импортированные повторно обновляют текущие.
Изменение типа элемента с товара на категорию или с категории на товар не допускается.
Порядок элементов в запросе является произвольным.

- uuid товара или категории является уникальным среди товаров и категорий
- родителем товара или категории может быть только категория
- принадлежность к категории определяется полем parentId
- товар или категория могут не иметь родителя
- название элемента не может быть null
- у категорий поле price должно содержать null
- цена товара не может быть null и должна быть больше либо равна нулю.
- при обновлении товара/категории обновленными считаются **все** их параметры
- при обновлении параметров элемента обязательно обновляется поле **date** в соответствии с временем обновления
- в одном запросе не может быть двух элементов с одинаковым id
- дата должна обрабатываться согласно ISO 8601 (такой придерживается OpenAPI). Если дата не удовлетворяет данному формату, необходимо отвечать 400.

Гарантируется, что во входных данных нет циклических зависимостей и поле updateDate монотонно возрастает. 
Гарантируется, что при проверке передаваемое время кратно секундам."""


@router.post("", responses=responses, response_class=Response, description=description)
@remove_422
async def create_shop_unit_type(
        shop_unit_items: ShopUnitImportRequest,
        shop_unit_repository: ShopUnitRepository = Depends(get_shop_unit_repository),
        children_repository: ChildrenRepository = Depends(get_children_repository),
):
    date = shop_unit_items.updateDate
    parent_id_list = set()
    for item in shop_unit_items.items:
        if await shop_unit_repository.get_by_id(item.id):
            await shop_unit_repository.update(item, date)
            await children_repository.update(item)
        else:
            await shop_unit_repository.create(item, date)
            await children_repository.create(item)

        if item.parentId:
            parent_id_list.add(item.parentId)

    for parent_id in parent_id_list:
        await shop_unit_repository.update_parent(parent_id, date)

    return
