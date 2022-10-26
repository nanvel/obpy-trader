from pydantic import BaseSettings, Field


class StorageSettings(BaseSettings):
    prefix: str = Field(env="storage_prefix", default="")

    # fs
    fs_root: str = Field(env="storage_fs_root", default=".storage")
