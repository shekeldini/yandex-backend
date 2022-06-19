import os
from datetime import timedelta

from dotenv import load_dotenv
from starlette.config import Config

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

config = Config(".env")
DATABASE_URL = config("DATABASE_URL", cast=str, default="")
SECRET_KEY = config("SECRET_KEY", cast=str, default="")
REDIS_URL = config("REDIS_URL", cast=str, default="")
REDIS_PORT = config("REDIS_PORT", cast=str, default="")

IMPORT_MAX_REQUESTS = 1000
IMPORT_EXPIRE = timedelta(minutes=60)
IMPORT_KEY = "IMPORT"

DELETE_MAX_REQUESTS = 1000
DELETE_EXPIRE = timedelta(minutes=60)
DELETE_KEY = "DELETE"

INFO_MAX_REQUESTS = 100
INFO_EXPIRE = timedelta(minutes=1)
INFO_KEY = "INFO"

DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.000Z"
