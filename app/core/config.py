import os

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., env='DATABASE_URL')
    SECRET_KEY: str = Field(..., env='SECRET_KEY')


settings = Settings()

