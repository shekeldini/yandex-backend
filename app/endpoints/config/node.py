from app.models.Error import Error

# response for route
RESPONSES = {
    200: {
        "description": "Статистика по элементу.",
    },
    400: {
        "model": Error,
        "description": "Некорректный формат запроса или некорректные даты интервала.",
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
DESCRIPTION = """Получение статистики (истории обновлений) по цене товара/категории за заданный интервал.
Статистика по удаленным элементам недоступна.

- цена категории - это средняя цена всех её товаров, включая товары дочерних категорий.Если категория не содержит товаров цена равна null. При обновлении цены товара, средняя цена категории, которая содержит этот товар, тоже обновляется.
- можно получить статистику за всё время."""