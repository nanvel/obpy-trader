from decimal import Decimal

import pandas as pd

from ob.models import ObpyCode, OrderBook, Symbol


class OrderBookFactory:
    def from_line(self, line: str, symbol: Symbol) -> OrderBook:
        assert line[0] == ObpyCode.ORDER_BOOK

        code, ts, *quantities = line.split(" ")

        bottom = Decimal(quantities[0].split(":")[0])
        top = Decimal(quantities[-1].split(":")[0])

        df = pd.DataFrame(
            (
                (bottom + i * symbol.price_tick, Decimal(0.0))
                for i in range(int((top - bottom) / symbol.price_tick) + 1)
            ),
            columns=["price", "quantity"],
        ).set_index("price")

        for r in quantities:
            p, q = r.split(":")
            df.at[Decimal(p), "quantity"] = Decimal(q)

        return OrderBook(ts=int(ts), update_id=0, df=df)
