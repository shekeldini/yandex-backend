from app.models.Error import Error
# response for route
RESPONSES = {
    200: {
        "description": "Информация об элементе.",
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

# description for route
DESCRIPTION = """Получить информацию об элементе по идентификатору. При получении информации о категории также предоставляется информация о её дочерних элементах.

- цена категории - это средняя цена всех её товаров, включая товары дочерних категорий.
Если категория не содержит товаров цена равна null.
При обновлении цены товара, средняя цена категории, которая содержит этот товар, тоже обновляется."""
