from databases import Database
from sqlalchemy import MetaData
from app.core.config import setting
from redis import Redis
# Metadata using for create sqlalchemy tables
metadata = MetaData()

# Postgresql connection
database = Database(setting.DATABASE_URL)

# Redis connection
redis = Redis(host=setting.REDIS_URL, port=setting.REDIS_PORT)
