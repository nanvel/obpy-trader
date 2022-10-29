from decimal import Decimal

from ob.models import ObpyCode, Trade


class TradeFactory:
    def from_line(self, line):
        code, ts, price, quantity = line.split(" ")

        assert code == ObpyCode.TRADE

        return Trade(
            ts=int(ts),
            price=Decimal(price),
            quantity=Decimal(quantity),
        )
