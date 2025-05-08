from abc import ABC, abstractmethod
from datetime import date


class StockPricePort(ABC):
    @abstractmethod
    def get_price(self, symbol: str, d: date) -> float:
        pass
