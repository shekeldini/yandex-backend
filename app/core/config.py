from datetime import timedelta
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env='DATABASE_URL')
    REDIS_URL: str = Field(..., env='REDIS_URL')
    REDIS_PORT: str = Field(..., env='REDIS_PORT')

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
