from decimal import Decimal

from ob.models.trade import Trade


class TradeFactory:
    def from_agg_trade(self, agg_trade) -> Trade:
        data = agg_trade["data"]

        return Trade(
            ts=data["E"],
            price=Decimal(data["p"]),
            quantity=Decimal(data["q"]) if data["m"] else Decimal("-" + data["q"]),
        )
