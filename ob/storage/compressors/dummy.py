from typing import TextIO

from .base import BaseCompressor


class DummyCompressor(BaseCompressor):
    def call(self, f: TextIO) -> TextIO:
        return f

    def rename(self, name: str) -> str:
        return name
