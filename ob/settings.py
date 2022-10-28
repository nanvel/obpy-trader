from pydantic import BaseSettings
from ob.storage.settings import StorageSettings


class Settings(BaseSettings):
    storage: StorageSettings = StorageSettings()
