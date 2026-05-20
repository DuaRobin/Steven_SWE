import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

env_state = os.getenv(key="ENVIRONMENT", default="development").lower()


class AppSettings(BaseSettings):
    app_name: str
    app_version: str
    environment: str = Field(env="ENVIRONMENT", default=env_state)
    ml_model_id: str
    model_config = SettingsConfigDict(
        env_file=(".env", f".env.{env_state}"), env_file_encoding="utf-8"
    )


app_settings = AppSettings()
