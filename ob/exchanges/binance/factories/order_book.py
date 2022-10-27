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

        for b in depth["bids"]:
            df.at[Decimal(b[0]), "quantity"] = Decimal("-" + b[1])

        for a in depth["asks"]:
            df.at[Decimal(a[0]), "quantity"] = Decimal(a[1])

        return OrderBook(
            symbol=symbol, update_id=depth["lastUpdateId"], df=df, ts=time.time()
        )
