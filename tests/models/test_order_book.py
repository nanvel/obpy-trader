from decimal import Decimal

import pandas as pd

from ob.models import OrderBook


def test_order_book():
    order_book = OrderBook(
        ts=1666858861088,
        df=pd.DataFrame(
            ((Decimal(i * 10), Decimal(i * 1)) for i in range(4)),
            columns=["price", "quantity"],
        ).set_index("price"),
        update_id=26350790110,
    )

    assert order_book.to_line() == "O 1666858861088 1E+1:1 2E+1:2 3E+1:3"
