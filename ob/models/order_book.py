import typing

from pydantic import BaseModel

from .symbol import Symbol


class OrderBook(BaseModel):
    update_id: int
    symbol: Symbol
    df: typing.Any
    ts: int
