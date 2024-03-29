from app.models.Error import Error
# response for route
RESPONSES = {
    200: {
        "description": "Список товаров, цена которых была обновлена.",
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
    }
}

# description for route
DESCRIPTION = """Получение списка **товаров**, цена которых была обновлена за последние 24 часа от времени переданном в запросе.
Обновление цены не означает её изменение.
Обновления цен удаленных товаров недоступны.
При обновлении цены товара, средняя цена категории, которая содержит этот товар, тоже обновляется."""
