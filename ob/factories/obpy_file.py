import os
import time

from ob.models import ObpyFile


class ObpyFileFactory:
    def __init__(self, fs_root: str, extension: str):
        self.fs_root = fs_root
        self.extension = extension

    def from_symbol(self, exchange_slug, symbol_slug):
        obpy_file = ObpyFile(
            fs_root=self.fs_root,
            exchange_slug=exchange_slug,
            symbol_slug=symbol_slug,
            ts_start=round(time.time() * 1000),
            extension=self.extension,
        )

        os.makedirs(os.path.dirname(obpy_file.temp_path), exist_ok=True)

        return obpy_file

    def from_path(self, path):
        *other, exchange_slug, symbol_slug, date_str, file_name = path.split(
            os.path.sep
        )
        file_name, ext = file_name.split(".")
        assert "." + ext == self.extension

        ts_start, ts_stop = file_name.split("_")

        return ObpyFile(
            fs_root=self.fs_root,
            exchange_slug=exchange_slug,
            symbol_slug=symbol_slug,
            ts_start=int(ts_start),
            ts_stop=int(ts_stop) if ts_stop != "temp" else None,
            extension=self.extension,
        )
