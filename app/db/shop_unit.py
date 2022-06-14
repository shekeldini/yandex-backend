from sqlalchemy import Table, String, Column, INTEGER
from .base import metadata

shop_unit = Table(
    "shop_unit",
    metadata,
    Column("id", String, primary_key=True, unique=True),
    Column("date", String, nullable=False),
    Column("name", String, nullable=False),
    Column("price", INTEGER, nullable=True),
    Column("type", String, nullable=False)
)
