from copy import deepcopy
from typing import Optional, Any
from uuid import UUID
from pydantic import BaseModel, root_validator

from app.models.ShopUnitType import ShopUnitType


class ShopUnitImport(BaseModel):
    id: UUID
    name: str
    parentId: Optional[UUID] = None
    type: ShopUnitType
    price: Optional[int] = None

    @root_validator
    def price_validation(cls, values):
        type, price = values.get("type"), values.get("price")
        if type.value == ShopUnitType.CATEGORY.value and (price or price == 0):
            raise ValueError('Validation Failed')
        if type.value == ShopUnitType.OFFER.value and (not price or price < 0):
            raise ValueError('Validation Failed')
        return values

    @classmethod
    def unvalidated(cls, **data: Any):
        for name, field in cls.__fields__.items():
            try:
                data[name]
            except KeyError:
                if field.required:
                    raise TypeError(f"Missing required keyword argument {name!r}")
                if field.default is None:
                    # deepcopy is quite slow on None
                    value = None
                else:
                    value = deepcopy(field.default)
                data[name] = value
        self = cls.__new__(cls)
        object.__setattr__(self, "__dict__", data)
        object.__setattr__(self, "__fields_set__", set(data.keys()))
        return self
