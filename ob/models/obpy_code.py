from enum import Enum


class ObpyCode(str, Enum):
    """.obpy format file codes."""

    EXCHANGE = "E"
    ORDER_BOOK = "O"
    SYMBOL = "S"
    TRADE = "T"
    UPDATES = "U"
    QUIT = "Q"
