from app.db.base import database
from app.repositories.children import ChildrenRepository
from app.repositories.shop_unit import ShopUnitRepository

from app.repositories.shop_unit_type import ShopUnitTypeRepository


def get_shop_unit_type_repository() -> ShopUnitTypeRepository:
    return ShopUnitTypeRepository(database)


# def get_shop_unit_import_request_repository() -> ShopUnitImportRequestRepository:
#     return ShopUnitImportRequestRepository(database)


def get_shop_unit_repository() -> ShopUnitRepository:
    return ShopUnitRepository(database)


def get_children_repository() -> ChildrenRepository:
    return ChildrenRepository(database)
