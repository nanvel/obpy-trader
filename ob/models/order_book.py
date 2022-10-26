import typing

from pydantic import BaseModel

from .symbol import Symbol


class OrderBook(BaseModel):
    symbol: Symbol
    df: typing.Any
    ts: int
