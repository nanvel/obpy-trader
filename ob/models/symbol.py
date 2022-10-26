from pydantic import BaseModel

from decimal import Decimal


class Symbol(BaseModel):
    slug: str
    base: str
    quote: str
    price_tick: Decimal

    def to_row(self):
        return f"S {self.slug} Q:{self.quote} B:{self.base} PT:{self.price_tick}"
