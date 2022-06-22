from sqlalchemy import Table, String, Column, INTEGER, DateTime
from .base import metadata


# Statistic table that stores all changes in OFFER and CATEGORY
statistic = Table(
    "statistic",
    metadata,
    Column("id", String),
    Column("name", String),
    Column("date", DateTime),
    Column("parent_id", String),
    Column("price", INTEGER),
    Column("type", String),
)
