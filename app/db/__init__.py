from .base import engine

# create tables if not exist
engine.execute(open("app/db/create_tables.sql", "r").read())
