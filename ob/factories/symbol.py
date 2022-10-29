from decimal import Decimal

from ob.models import ObpyCode, Symbol


class SymbolFactory:
    def from_line(self, line) -> Symbol:
        code, slug, *params = line.split(' ')

        assert code == ObpyCode.SYMBOL

        params = {
            k: v
            for k, v in (p.split(':') for p in params)
        }

        return Symbol(
            slug=slug,
            quote=params['Q'],
            base=params['B'],
            price_tick=Decimal(params['PT'])
        )
