import os

from pydantic import BaseSettings, Field, validator


class StorageSettings(BaseSettings):
    fs_root: str = Field(default=".storage")
    uploads_table_name: str
    s3_bucket_name: str

    @validator("fs_root")
    def validate_fs_root(cls, fs_root):
        """Convert to absolute path and check if the folder exist."""
        root = os.path.realpath(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), "../..", fs_root)
        )

        assert os.path.isdir(root), "Path does not exist!"

        return root

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        env_prefix = "storage_"
