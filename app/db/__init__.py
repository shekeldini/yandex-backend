from .base import engine

# create tables if not exist
engine.execute(open("db/create_tables.sql", "r").read())
