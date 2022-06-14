from pydantic import BaseModel, Field
from uuid import UUID


class Delete(BaseModel):
    id: UUID = Field(default="3fa85f64-5717-4562-b3fc-2c963f66a333",
                     nullable=False,
                     description="Идентификатор элемента")
