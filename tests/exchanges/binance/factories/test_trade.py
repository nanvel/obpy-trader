from decimal import Decimal

from ob.exchanges.binance import TradeFactory
from ob.models import Trade


def test_order_book_factory(data):
    agg_trade = data.load("binance", "agg_trade_btcusdt")

    factory = TradeFactory()
    trade = factory.from_agg_trade(agg_trade)

    assert isinstance(trade, Trade)
    assert trade.dict() == {
        "price": Decimal("20715.3"),
        "quantity": Decimal("-0.00295"),
        "ts": 1666858861139,
    }

    assert trade.to_line() == "T 1666858861139 20715.3 -0.00295"
