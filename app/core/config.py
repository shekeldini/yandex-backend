from datetime import timedelta
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    DATABASE_URL: str = Field(default="postgresql://user:password@10.21.0.150:5432/yandex_db")
    REDIS_URL: str = Field(default="10.21.0.150")
    REDIS_PORT: int = Field(default=6379)

    IMPORT_MAX_REQUESTS: int = Field(default=1000)
    IMPORT_EXPIRE: timedelta = Field(default=timedelta(minutes=60))
    IMPORT_KEY: str = Field(default="IMPORT")

    DELETE_MAX_REQUESTS: int = Field(default=1000)
    DELETE_EXPIRE: timedelta = Field(default=timedelta(minutes=60))
    DELETE_KEY: str = Field(default="DELETE")

    INFO_MAX_REQUESTS: int = Field(default=100)
    INFO_EXPIRE: timedelta = Field(default=timedelta(minutes=1))
    INFO_KEY: str = Field(default="INFO")

    DATE_TIME_FORMAT: str = Field(default="%Y-%m-%dT%H:%M:%S.000Z")


setting = Settings()
