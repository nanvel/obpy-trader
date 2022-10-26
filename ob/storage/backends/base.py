from abc import ABC, abstractmethod
from typing import AsyncGenerator, List


class BaseReader(ABC):
    @classmethod
    @abstractmethod
    def init(cls, *args, **kwargs) -> "BaseReader":
        pass

    @abstractmethod
    async def read(self) -> AsyncGenerator[str]:
        pass

    @abstractmethod
    async def __aenter__(self):
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass


class BaseWriter(ABC):
    @classmethod
    @abstractmethod
    def init(cls, *args, **kwargs) -> "BaseWriter":
        pass

    @abstractmethod
    async def write(self, lines: List[str]) -> None:
        pass

    @abstractmethod
    async def __aenter__(self):
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
