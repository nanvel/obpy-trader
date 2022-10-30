from ob.factories import TradeFactory
from ob.models import Trade


def test_trade_factory():
    factory = TradeFactory()

    trade = factory.from_line("T 1666858861139 20715.3 -0.00295")

    assert isinstance(trade, Trade)
