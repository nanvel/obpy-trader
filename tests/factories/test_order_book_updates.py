from ob.models import OrderBookUpdates
from ob.factories import OrderBookUpdatesFactory


def test_order_book_updates():
    factory = OrderBookUpdatesFactory()

    line = (
        "U 1666858861088 20673.18:0 20683.09:0.01574 20715.17:0.00096 "
        "20715.18:0.08415 20715.21:-0 20715.32:-0 20770.43:-5.31165 93211:-0.01"
    )

    updates = factory.from_line(line)

    assert isinstance(updates, OrderBookUpdates)
