import os
from pathlib import Path
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

env_state = os.getenv(key="ENVIRONMENT", default="development").lower()

# Define the workspace directory for loading .env files
WORKSPACE_DIR = Path(__file__).resolve().parents[1]

class AppSettings(BaseSettings):
    app_name: str
    app_version: str
    environment: str = Field(env="ENVIRONMENT", default=env_state)
    google_cloud_project: str
    google_cloud_location: str
    google_genai_use_vertexai: bool
    log_level: str
    embedding_model_name: str
    model_name: str
    model_config = SettingsConfigDict(
        env_file=(f"{WORKSPACE_DIR}/.env", f"{WORKSPACE_DIR}/.env.{env_state}"),
        env_file_encoding="utf-8",
    )


app_settings = AppSettings()
