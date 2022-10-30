from typing import BinaryIO

from .base import BaseCompressor


class DummyCompressor(BaseCompressor):
    encoding = None

    def call(self, f: BinaryIO) -> BinaryIO:
        return f

    def rename(self, name: str) -> str:
        return name
