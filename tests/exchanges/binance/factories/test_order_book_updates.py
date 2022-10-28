from decimal import Decimal

from ob.exchanges.binance import OrderBookUpdatesFactory
from ob.models import OrderBookUpdates


def test_order_book_updates_factory(data):
    depth_update = data.load("binance", "depth_update_btcusdt")

    factory = OrderBookUpdatesFactory()
    updates = factory.from_depth_update(depth_update)

    assert isinstance(updates, OrderBookUpdates)
    assert updates.dict() == {
        "update_id": 26357061087,
        "ts": 1666858861088,
        "updates": {
            Decimal("20715.18000000"): Decimal("0.08415000"),
            Decimal("20715.17000000"): Decimal("0.00096000"),
            Decimal("20683.09000000"): Decimal("0.01574000"),
            Decimal("20673.18000000"): Decimal("0E-8"),
            Decimal("20715.21000000"): Decimal("-0E-8"),
            Decimal("20715.32000000"): Decimal("-0E-8"),
            Decimal("20770.43000000"): Decimal("-5.31165000"),
            Decimal("93211.00000000"): Decimal("-0.01000000"),
        },
    }

    assert updates.to_line() == (
        "U 1666858861088 20673.18:0 20683.09:0.01574 20715.17:0.00096 "
        "20715.18:0.08415 20715.21:-0 20715.32:-0 20770.43:-5.31165 93211:-0.01"
    )
