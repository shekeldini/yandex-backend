from databases import Database
from sqlalchemy import MetaData
from app.core.config import settings

database = Database(settings.DATABASE_URL)
metadata = MetaData()
