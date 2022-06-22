from app.models.Error import Error

# response for route
RESPONSES = {
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

# description for route
DESCRIPTION = """Удалить элемент по идентификатору. При удалении категории удаляются все дочерние элементы. 
Доступ к статистике (истории обновлений) удаленного элемента невозможен.

**Обратите, пожалуйста, внимание на этот обработчик. При его некорректной работе тестирование может быть невозможно.**"""
