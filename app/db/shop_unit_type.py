from sqlalchemy import Table, String, Column
from .base import metadata

shop_unit_type = Table(
    "shop_unit_type",
    metadata,
    Column("shop_unit_type", String, primary_key=True, unique=True)
)
