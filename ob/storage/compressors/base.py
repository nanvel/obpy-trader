from abc import ABC, abstractmethod
from typing import BinaryIO, TextIO


class BaseCompressor(ABC):
    @abstractmethod
    def call(self, f: TextIO) -> BinaryIO | TextIO:
        pass

    @abstractmethod
    def rename(self, name: str) -> str:
        pass
