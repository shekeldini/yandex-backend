from fastapi import Path
from uuid import UUID

from pydantic.dataclasses import dataclass


@dataclass
class Delete:
    id: UUID = Path(example="3fa85f64-5717-4562-b3fc-2c963f66a333",
                    description="Идентификатор")
