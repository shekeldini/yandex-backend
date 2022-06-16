from app.db.base import database
from app.repositories.children import ChildrenRepository
from app.repositories.sales import SalesRepository
from app.repositories.shop_unit import ShopUnitRepository
from app.repositories.nodes import NodesRepository


def get_shop_unit_repository() -> ShopUnitRepository:
    return ShopUnitRepository(database)


def get_children_repository() -> ChildrenRepository:
    return ChildrenRepository(database)


def get_nodes_repository() -> NodesRepository:
    return NodesRepository(database)


def get_sales_repository() -> SalesRepository:
    return SalesRepository(database)
