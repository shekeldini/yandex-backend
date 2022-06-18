from sqlalchemy import Table, String, Column, INTEGER, DateTime
from .base import metadata

statistic = Table(
    "statistic",
    metadata,
    Column("id", String),
    Column("name", String),
    Column("date", DateTime),
    Column("parentId", String),
    Column("price", INTEGER),
    Column("type", String),
)
