from decimal import Decimal

from ob.factories import OrderBookFactory
from ob.models import OrderBook, Symbol


def test_order_book_factory():
    line = "O 1666858861088 1E+1:1 2E+1:2 3E+1:3"

    factory = OrderBookFactory()

    symbol = Symbol(
        slug="BTCUSDT", quote="USDT", base="BTC", price_tick=Decimal("1")
    )

    order_book = factory.from_line(line=line, symbol=symbol)

    assert isinstance(order_book, OrderBook)
