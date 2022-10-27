from decimal import Decimal
from typing import Dict

from pydantic import BaseModel

from .obpy_code import ObpyCode


class OrderBookUpdates(BaseModel):
    update_id: int
    ts: int
    updates: Dict[Decimal, Decimal]

    def to_line(self):
        updates = sorted(list(self.updates.items()), key=lambda i: i[0])

        return (
            f"{ObpyCode.UPDATE} {self.ts} "
            f"{' '.join([f'{p.normalize()}:{q.normalize()}' for p, q in updates])}"
        )
