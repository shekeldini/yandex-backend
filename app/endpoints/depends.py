from app.db.base import database
from app.repositories.shop_unit_import_request import ShopUnitImportRequestRepository
from app.repositories.shop_unit_type import ShopUnitTypeRepository


def get_shop_unit_type_repository() -> ShopUnitTypeRepository:
    return ShopUnitTypeRepository(database)


def get_shop_unit_import_request_repository() -> ShopUnitImportRequestRepository:
    return ShopUnitImportRequestRepository(database)
