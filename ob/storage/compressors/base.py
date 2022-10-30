from abc import ABC, abstractmethod
from typing import BinaryIO


class BaseCompressor(ABC):
    @abstractmethod
    def call(self, f: BinaryIO) -> BinaryIO:
        pass

    @abstractmethod
    def rename(self, name: str) -> str:
        pass

    @property
    @abstractmethod
    def encoding(self) -> str | None:
        pass
