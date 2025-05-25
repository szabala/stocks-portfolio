from ports.stock_price_port import StockPricePort
from datetime import date
import random


class DummyStockPriceProvider(StockPricePort):
    def get_price(self, symbol: str, d: date) -> float:
        return random.uniform(100, 500)
