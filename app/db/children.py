from sqlalchemy import Table, String, Column, ForeignKey
from .base import metadata


# Сhildrens table where OFFER and CATEGORY are linked
children = Table(
    "childrens",
    metadata,
    Column("children_id", String, primary_key=True),
    Column("parent_id", String, primary_key=True)
)
