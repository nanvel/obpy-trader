import os
from io import TextIOWrapper
from typing import AsyncGenerator, List, Optional

from ..factories.file_name import FileNameFactory
from .base import BaseReader, BaseWriter


class FsReader(BaseReader):
    def __init__(self, path):
        self.path = path
        self._file: Optional[TextIOWrapper] = None

    @classmethod
    async def init(cls, path) -> "BaseReader":
        async with cls(path) as reader:
            yield reader

    async def read(self) -> AsyncGenerator[str, None]:
        for line in self._file:
            yield line

    async def __aenter__(self):
        self._file = open(self.path, "r")

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._file is not None:
            self._file.close()


class FsWriter(BaseWriter):
    def __init__(self, root_path: str, file_name_factory: FileNameFactory, ts: int):
        self.path = os.path.join(root_path, file_name_factory.from_time(ts))
        self._file: Optional[TextIOWrapper] = None

    @classmethod
    async def init(
        cls, root_path: str, file_name_factory: FileNameFactory, ts: int
    ) -> "BaseWriter":
        async with cls(
            root_path=root_path, file_name_factory=file_name_factory, ts=ts
        ) as writer:
            yield writer

    async def write(self, lines: List[str]) -> None:
        self._file.writelines((i + "\n" for i in lines))

    async def __aenter__(self):
        self._file = open(self.path, "w")

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._file is not None:
            self._file.close()