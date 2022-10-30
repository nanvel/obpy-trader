from decimal import Decimal

from ob.models import Symbol
from ob.storage.use_cases.build_file_path import BuildFilePath


def test_build_file_path():
    use_case = BuildFilePath(extension=".obpy", prefix="")

    symbol = Symbol(slug="BTCUSDT", quote="USDT", base="BTC", price_tick=Decimal("1"))

    path = use_case.call(exchange="binance", symbol=symbol, ts=1667110871)

    assert path == "binance/BTCUSDT/2022-10-30/1667110871.obpy"
