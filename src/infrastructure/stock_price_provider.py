from ports.stock_price_port import StockPricePort
from datetime import date


class DummyStockPriceProvider(StockPricePort):
    def get_price(self, symbol: str, d: date) -> float:
        return 100.0
