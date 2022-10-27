from decimal import Decimal

from ob.models import OrderBookUpdates


class OrderBookUpdatesFactory:
    def from_depth_update(self, depth_update) -> OrderBookUpdates:
        data = depth_update["data"]

        updates = {}
        for p, q in data["b"]:
            updates[Decimal(p)] = Decimal(q)

        for p, q in data["a"]:
            updates[Decimal(p)] = Decimal("-" + q)

        return OrderBookUpdates(update_id=data["u"], ts=data["E"], updates=updates)
