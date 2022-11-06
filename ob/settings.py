from pydantic import BaseSettings
from ob.storage.settings import StorageSettings


class Settings(BaseSettings):
    storage: StorageSettings = StorageSettings()

    aws_region: str = "ap-southeast-1"
    aws_access_key: str | None = None
    aws_secret_key: str | None = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
