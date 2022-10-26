from asyncio import Queue
from abc import ABC, abstractmethod

from ob.models import OrderBook, Symbol


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

    def to_row(self):
        return f"E {self.slug}"
