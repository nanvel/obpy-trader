from decimal import Decimal

from pydantic import BaseModel

from .obpy_code import ObpyCode


class Symbol(BaseModel):
    slug: str
    base: str
    quote: str
    price_tick: Decimal

    def to_row(self):
        return f"{ObpyCode.SYMBOL} {self.slug} Q:{self.quote} B:{self.base} PT:{self.price_tick}"
