from databases import Database
from sqlalchemy import MetaData, create_engine
from app.core.config import setting
from redis import Redis
# Metadata using for create sqlalchemy tables
metadata = MetaData()

# Postgresql connection
database = Database(setting.DATABASE_URL)

# Redis connection
redis = Redis(host=setting.REDIS_URL, port=setting.REDIS_PORT)

# synchronous engine for create tables
engine = create_engine(
    setting.DATABASE_URL
)