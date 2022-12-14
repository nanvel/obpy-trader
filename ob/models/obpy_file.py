import os
from datetime import datetime

import pytz
from pydantic import BaseModel


class ObpyFile(BaseModel):
    fs_root: str
    exchange_slug: str
    symbol_slug: str
    ts_start: int
    ts_stop: int | None = None
    extension: str
    ts_latest: int = 0

    @property
    def temp_path(self) -> str:
        return os.path.join(
            self.fs_root,
            self.exchange_slug,
            self.symbol_slug,
            self._date_str,
            f"{self.ts_start}_temp{self.extension}",
        )

    @property
    def fs_path(self) -> str:
        return os.path.join(
            self.fs_root,
            self.exchange_slug,
            self.symbol_slug,
            self._date_str,
            f"{self.ts_start}_{self.ts_stop}{self.extension}",
        )

    @property
    def cloud_path(self) -> str:
        return os.path.join(
            self.exchange_slug,
            self.symbol_slug,
            self._date_str,
            f"{self.ts_start}_{self.ts_stop}{self.extension}",
        )

    @property
    def is_temp(self) -> bool:
        return self.ts_stop is None

    @property
    def _date_str(self) -> str:
        return datetime.fromtimestamp(self.ts_start // 1000, pytz.utc).strftime(
            "%Y-%m-%d"
        )

    @property
    def _stop_str(self) -> str | int:
        return "temp" if self.is_temp else self.ts_stop

    def update_ts(self, ts):
        self.ts_latest = ts or self.ts_latest

    def finalize(self):
        _ts_stop = self.ts_stop
        self.ts_stop = self.ts_latest

        fs_path = self.fs_path

        try:
            assert not os.path.exists(fs_path)

            os.makedirs(os.path.dirname(fs_path), exist_ok=True)
            os.rename(self.temp_path, fs_path)
        except OSError:
            self.ts_stop = _ts_stop
