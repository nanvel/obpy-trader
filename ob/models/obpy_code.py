from enum import Enum


class ObpyCode(str, Enum):
    """.obpy format file codes."""

    EXCHANGE = "E"
    ORDER_BOOK = "O"
    SYMBOL = "S"
    TRADES = "T"
    UPDATE = "U"
    QUIT = "Q"
