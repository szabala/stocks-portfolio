from .entities import Stock
from typing import List, Dict
from exceptions.domain import RebalanceError


class Portfolio:
    def __init__(self, stocks: List[Stock], allocation: Dict[str, float]):
        self.stocks = stocks
        self.allocation = allocation

    def value(self, price_provider) -> float:
        return sum(
            stock.quantity * stock.current_price(price_provider)
            for stock in self.stocks
        )

    def rebalance(self) -> Dict[str, float]:
        if not self.allocation:
            raise RebalanceError("No allocation provided for rebalancing.")

        total_shares = sum(stock.quantity for stock in self.stocks)
        if total_shares == 0:
            raise RebalanceError("No shares in portfolio to rebalance.")

        target_shares = {
            symbol: total_shares * weight for symbol, weight in self.allocation.items()
        }
        current_shares = {stock.symbol: stock.quantity for stock in self.stocks}

        rebalance = {
            symbol: target_shares[symbol] - current_shares.get(symbol, 0)
            for symbol in self.allocation
        }

        return rebalance
