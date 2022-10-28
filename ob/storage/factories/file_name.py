from datetime import datetime

import pytz


class FileNameFactory:
    def __init__(self, prefix: str, extension: str):
        self.prefix = prefix
        self.extension = extension

    def from_time(self, time: int) -> str:
        time_str = datetime.fromtimestamp(time, pytz.utc).strftime("%Y-%m-%dT%H:%M:%S")

        return f"{self.prefix}{time_str}{self.extension}"
