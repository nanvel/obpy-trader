import time
from decimal import Decimal

import pandas as pd

from ob.models import OrderBook, Symbol


class OrderBookFactory:
    def from_depth(self, depth, symbol: Symbol) -> OrderBook:
        top = Decimal(depth["asks"][-1][0])
        bottom = Decimal(depth["bids"][-1][0])

        df = pd.DataFrame(
            (
                (bottom + i * symbol.price_tick, Decimal(0.0))
                for i in range(int((top - bottom) / symbol.price_tick) + 1)
            ),
            columns=["price", "quantity"],
        ).set_index("price")

        for p, q in depth["bids"]:
            df.at[Decimal(p), "quantity"] = Decimal("-" + q)

        for p, q in depth["asks"]:
            df.at[Decimal(p), "quantity"] = Decimal(q)

        return OrderBook(update_id=depth["lastUpdateId"], df=df, ts=time.time())
