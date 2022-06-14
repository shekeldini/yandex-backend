from databases import Database
from sqlalchemy import MetaData
from app.core.config import DATABASE_URL, REDIS_URL, REDIS_PORT
from redis import Redis

metadata = MetaData()
database = Database(DATABASE_URL)
redis = Redis(host=REDIS_URL, port=REDIS_PORT)
