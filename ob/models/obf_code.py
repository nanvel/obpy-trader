from enum import Enum


class ObfCode(str, Enum):
    """Order book format file codes."""

    EXCHANGE = "E"
    ORDER_BOOK = "O"
    SYMBOL = "S"
    TRADES = "T"
    UPDATE = "U"
    QUIT = "Q"
