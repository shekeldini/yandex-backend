from sqlalchemy import Table, String, Column, ForeignKey
from .base import metadata

children = Table(
    "childrens",
    metadata,
    Column("children_id", String, ForeignKey("shop_unit.id"), primary_key=True),
    Column("parent_id", String, ForeignKey("shop_unit.id"), primary_key=True)
)
