from typing import List

from ..backends.base import BaseReader


class ReaderService:
    def __init__(self, backends: List[BaseReader]):
        self.backends = backends
