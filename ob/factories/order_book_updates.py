from decimal import Decimal

from ob.models import ObpyCode, OrderBookUpdates


class OrderBookUpdatesFactory:
    def from_line(self, line):
        code, ts, *args = line.split(' ')

        assert code == ObpyCode.UPDATES

        return OrderBookUpdates(
            update_id=0,
            ts=int(ts),
            updates={
                Decimal(k): Decimal(v)
                for k, v in (i.split(':') for i in args)
            }
        )
