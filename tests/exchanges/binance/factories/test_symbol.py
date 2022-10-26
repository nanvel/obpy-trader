from decimal import Decimal

from ob.exchanges.binance.factories import SymbolFactory
from ob.models import Symbol


def test_symbol_factory(data):
    exchange_info = data.load("binance", "exchange_info_btcusdt")

    factory = SymbolFactory()
    symbol = factory.from_exchange_info(exchange_info, symbol="BTCUSDT")

    assert isinstance(symbol, Symbol)
    assert symbol.dict() == {
        "base": "BTC",
        "price_tick": Decimal("0.01"),
        "quote": "USDT",
        "slug": "BTCUSDT",
    }
