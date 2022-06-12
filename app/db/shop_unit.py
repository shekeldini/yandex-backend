from sqlalchemy import Table, String, Column, INTEGER, ForeignKey
from .base import metadata

shop_unit = Table(
    "shop_unit",
    metadata,
    Column("id", String, primary_key=True, unique=True),
    Column("date", String, nullable=False),
    Column("name", String, nullable=False),
    Column("price", INTEGER, nullable=True),
    Column("shop_unit_type", String, ForeignKey('shop_unit_type.shop_unit_type'), nullable=False)
)
