from gzip import GzipFile
from io import BytesIO
from typing import BinaryIO, TextIO

from .base import BaseCompressor


class GzCompressor(BaseCompressor):
    def __init__(self, compress_level):
        self.compress_level = compress_level

    def call(self, f: TextIO) -> BinaryIO:
        mem = BytesIO()

        with GzipFile(fileobj=mem, mode="wb", compresslevel=self.compress_level) as gz:
            gz.write(f.read())

        mem.seek(0)

        return mem

    def rename(self, name: str) -> str:
        return name + ".gz"
