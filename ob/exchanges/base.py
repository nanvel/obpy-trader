from asyncio import Queue
from abc import ABC, abstractmethod

from ob.models import ObpyCode, Symbol


class BaseExchange(ABC):
    @property
    @abstractmethod
    def slug(self):
        pass

    @abstractmethod
    async def pull_symbol(self, symbol_slug) -> Symbol:
        pass

    @abstractmethod
    async def init_listener(self, symbol: Symbol) -> Queue:
        pass

    def to_line(self):
        return f"{ObpyCode.EXCHANGE} {self.slug}"
