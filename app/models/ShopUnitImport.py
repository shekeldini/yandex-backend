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
        # Category can't have price
        if type.value == ShopUnitType.CATEGORY.value and price is not None:
            raise ValueError('Validation Failed')
        # Offer price should be >= 0
        if type.value == ShopUnitType.OFFER.value and (price is None or price < 0):
            raise ValueError('Validation Failed')
        return values

    @classmethod
    def unvalidated(cls, **data: Any):
        """Using when calculate and update category price"""
        for name, field in cls.__fields__.items():
            try:
                data[name]
            except KeyError:
                if field.required:
                    raise TypeError(f"Missing required keyword argument {name!r}")
                if field.default is None:
                    value = None
                else:
                    value = deepcopy(field.default)
                data[name] = value
        self = cls.__new__(cls)
        object.__setattr__(self, "__dict__", data)
        object.__setattr__(self, "__fields_set__", set(data.keys()))
        return self
