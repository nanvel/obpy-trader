import os

from pydantic import BaseSettings, Field, validator


class StorageSettings(BaseSettings):
    prefix: str = Field(env="storage_prefix", default="")

    # fs
    fs_root: str = Field(env="storage_fs_root", default=".storage")

    @validator("fs_root")
    def validate_fs_root(cls, fs_root):
        """Convert to absolute path and check if the folder exist."""
        root = os.path.realpath(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "../..", fs_root)
        )

        assert os.path.isdir(root), "Path does not exist!"

        return root
