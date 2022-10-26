from io import TextIOWrapper
from typing import AsyncGenerator, List, Optional

from .base import BaseReader, BaseWriter


class FsReader(BaseReader):
    def __init__(self, path):
        self.path = path
        self._file: Optional[TextIOWrapper] = None

    @classmethod
    def init(cls, path) -> "BaseReader":
        with cls(path) as reader:
            yield reader

    async def read(self) -> AsyncGenerator[str]:
        for line in self._file:
            yield line

    async def __aenter__(self):
        self._file = open(self.path, "r")

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._file is not None:
            self._file.close()


class FsWriter(BaseWriter):
    def __init__(self, path):
        self.path = path
        self._file: Optional[TextIOWrapper] = None

    @classmethod
    def init(cls, path) -> "BaseWriter":
        with cls(path) as writer:
            yield writer

    async def write(self, lines: List[str]) -> None:
        self._file.writelines(lines)

    async def __aenter__(self):
        self._file = open(self.path, "w")

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._file is not None:
            self._file.close()
