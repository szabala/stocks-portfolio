from dataclasses import dataclass
from datetime import date
from ports.stock_price_port import StockPricePort


@dataclass
class Stock:
    symbol: str
    quantity: float

    def price(self, d: date, provider: StockPricePort) -> float:
        return provider.get_price(self.symbol, d)
