from pydantic import BaseModel, Field


class Error(BaseModel):
    code: int = Field(..., title=None, nullable=False)
    message: str = Field(..., title=None, nullable=False)
