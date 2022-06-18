from datetime import datetime
from typing import Optional
from fastapi import Path, Query
from uuid import UUID
from pydantic.dataclasses import dataclass


@dataclass
class StatisticRequest:
    id: UUID = Path(
        example="3fa85f64-5717-4562-b3fc-2c963f66a333",
        description="UUID товара/категории для которой будет отображаться статистика"
    )
    dateStart: Optional[datetime] = Query(
        default=None,
        example="2022-05-28T21:12:01.000Z",
        description="Дата и время начала интервала, для которого считается статистика. "
                    "Дата должна обрабатываться согласно ISO 8601 (такой придерживается OpenAPI). "
                    "Если дата не удовлетворяет данному формату, необходимо отвечать 400."
    )
    dateEnd: Optional[datetime] = Query(
        default=None,
        example="2022-05-28T21:12:01.000Z",
        description="Дата и время конца интервала, для которого считается статистика. "
                    "Дата должна обрабатываться согласно ISO 8601 (такой придерживается OpenAPI). "
                    "Если дата не удовлетворяет данному формату, необходимо отвечать 400."
    )

