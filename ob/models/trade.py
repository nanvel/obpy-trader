from decimal import Decimal

from pydantic import BaseModel

from .obpy_code import ObpyCode


class Trade(BaseModel):
    ts: int
    price: Decimal
    quantity: Decimal

    def to_line(self):
        return f"{ObpyCode.TRADE} {self.ts} {self.price.normalize()} {self.quantity.normalize()}"
