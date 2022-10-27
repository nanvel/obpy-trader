from decimal import Decimal

from ob.exchanges.binance import OrderBookFactory
from ob.models import OrderBook, Symbol


def test_order_book_factory(data):
    depth = data.load("binance", "depth_btcusdt")

    symbol = Symbol(
        slug="BTCUSDT", quote="USDT", base="BTC", price_tick=Decimal("0.01")
    )

    factory = OrderBookFactory()
    symbol = factory.from_depth(depth, symbol=symbol)

    assert isinstance(symbol, OrderBook)
