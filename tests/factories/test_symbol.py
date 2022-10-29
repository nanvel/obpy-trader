from ob.factories import SymbolFactory
from ob.models import Symbol


def test_symbol_factory():
    factory = SymbolFactory()

    symbol = factory.from_line(line="S BTCUSDT Q:USDT B:BTC PT:0.01")

    assert isinstance(symbol, Symbol)
