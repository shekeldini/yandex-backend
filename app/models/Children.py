from uuid import UUID

from pydantic import BaseModel


class Children(BaseModel):
    children_id: UUID
    parent_id: UUID
