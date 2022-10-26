from decimal import Decimal

from ob.models import Symbol


class SymbolFactory:
    def from_exchange_info(self, response, symbol) -> Symbol:
        symbol = next(filter(lambda i: i["symbol"] == symbol, response["symbols"]))
        price_filter = next(
            filter(lambda i: i["filterType"] == "PRICE_FILTER", symbol["filters"])
        )

        return Symbol(
            slug=symbol["symbol"],
            base=symbol["baseAsset"],
            quote=symbol["quoteAsset"],
            price_tick=Decimal(price_filter["tickSize"]),
        )
