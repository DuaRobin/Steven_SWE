import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

env_state = os.getenv(key="ENVIRONMENT", default="development").lower()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AppSettings(BaseSettings):
    app_name: str
    app_version: str
    environment: str = Field(env="ENVIRONMENT", default=env_state)
    google_cloud_project: str
    google_cloud_location: str
    google_genai_use_vertexai: bool
    log_level: str
    model_name: str
    model_config_temprature: float
    model_config_max_output_tokens: int
    data_store_id: str
    data_store_region: str
    model_config = SettingsConfigDict(
        env_file=(f"{BASE_DIR}/.env", f"{BASE_DIR}/.env.{env_state}"),
        env_file_encoding="utf-8",
    )


app_settings = AppSettings()
