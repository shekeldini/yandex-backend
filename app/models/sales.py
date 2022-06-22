from datetime import datetime
from fastapi import Query
from pydantic import validator
from pydantic.dataclasses import dataclass


@dataclass
class SalesDate:
    date: datetime = Query(
        example="2022-05-28T21:12:01.000Z",
        description="Дата и время запроса. "
                    "Дата должна обрабатываться согласно ISO 8601 (такой придерживается OpenAPI). "
                    "Если дата не удовлетворяет данному формату, необходимо отвечать 400"
    )

    @validator('date')
    def datetime_valid(cls, date: datetime):
        try:
            date.isoformat()
        except:
            raise ValueError('Validation Failed')
        return date
