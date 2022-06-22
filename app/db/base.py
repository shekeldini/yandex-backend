from databases import Database
from sqlalchemy import MetaData
from app.core.config import setting
from redis import Redis

metadata = MetaData()
database = Database(setting.DATABASE_URL)
redis = Redis(host=setting.REDIS_URL, port=setting.REDIS_PORT)
