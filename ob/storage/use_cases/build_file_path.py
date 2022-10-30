import os
from datetime import datetime

import pytz

from ob.models import Symbol


class BuildFilePath:
    def __init__(self, extension: str, prefix: str):
        self.extension = extension
        self.prefix = prefix

    def call(self, exchange: str, symbol: Symbol, ts: int):
        date_str = datetime.fromtimestamp(ts, pytz.utc).strftime("%Y-%m-%d")

        return os.path.join(
            self.prefix, exchange, symbol.slug, date_str, f"{ts}{self.extension}"
        )
