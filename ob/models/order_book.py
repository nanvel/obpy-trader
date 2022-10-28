import typing

from pydantic import BaseModel

from .obpy_code import ObpyCode


class OrderBook(BaseModel):
    df: typing.Any
    ts: int
    update_id: int

    def to_line(self):
        ob = " ".join(
            (
                f"{p.normalize()}:{q['quantity'].normalize()}"
                for p, q in self.df[self.df.quantity != 0].iterrows()
            )
        )

        return f"{ObpyCode.ORDER_BOOK} {self.ts} {ob}"
