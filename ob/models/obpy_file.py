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

    def finalize(self, ts_start: int, ts_stop: int):
        temp_path = self.temp_path

        _ts_start = self.ts_start
        _ts_stop = self.ts_stop

        self.ts_start = ts_start
        self.ts_stop = ts_stop

        fs_path = self.fs_path

        try:
            assert not os.path.exists(fs_path)

            os.makedirs(os.path.dirname(fs_path), exist_ok=True)
            os.rename(temp_path, fs_path)
        except OSError:
            self.ts_start = _ts_start
            self.ts_stop = _ts_stop
