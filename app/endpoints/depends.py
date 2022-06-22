from app.db.base import database
from app.repositories.children import ChildrenRepository
from app.repositories.node import NodeRepository
from app.repositories.sales import SalesRepository
from app.repositories.shop_unit import ShopUnitRepository
from app.repositories.nodes import NodesRepository


def get_shop_unit_repository() -> ShopUnitRepository:
    """
    Return Shop Unit Repository using for depends on routs
    """
    return ShopUnitRepository(database)


def get_children_repository() -> ChildrenRepository:
    """
        Return Children Repository using for depends on routs
    """
    return ChildrenRepository(database)


def get_nodes_repository() -> NodesRepository:
    """
        Return Nodes Repository using for depends on routs
    """
    return NodesRepository(database)


def get_sales_repository() -> SalesRepository:
    """
        Return Sales Repository using for depends on routs
    """
    return SalesRepository(database)


def get_node_repository() -> NodeRepository:
    """
        Return Node Repository using for depends on routs
    """
    return NodeRepository(database)
