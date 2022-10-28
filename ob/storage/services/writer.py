from typing import List

from ..backends.base import BaseWriter


class WriterService:
    def __init__(self, backends: List[BaseWriter]):
        self.backends = backends
