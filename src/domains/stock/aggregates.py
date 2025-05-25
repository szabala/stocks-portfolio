from ports.stock_price_port import StockPricePort
from .entities import Stock
from typing import List, Dict
from exceptions.domain import RebalanceError
from datetime import date


class Portfolio:
    def __init__(self, stocks: List[Stock], allocation: Dict[str, float]):
        self.stocks = stocks
        self.allocation = allocation

    def value(self, price_provider: StockPricePort) -> float:
        return sum(
            stock.quantity * stock.current_price(price_provider)
            for stock in self.stocks
        )

    def rebalance(self, price_provider: StockPricePort) -> Dict[str, float]:
        if not self.allocation:
            raise RebalanceError("No allocation provided for rebalancing.")

        # Get all symbols in allocation and stocks
        symbols = set(self.allocation.keys()) | {s.symbol for s in self.stocks}

        # Build a dict of Stock objects for all symbols
        stock_map = {stock.symbol: stock for stock in self.stocks}
        for symbol in symbols:
            if symbol not in stock_map:
                # Create a dummy Stock with quantity 0 for missing symbols
                stock_map[symbol] = Stock(symbol=symbol, quantity=0)

        # Get current prices using Stock.current_price
        prices = {symbol: stock_map[symbol].current_price(price_provider) for symbol in symbols}

        # Calculate current value for each stock in portfolio
        current_shares = {symbol: stock_map[symbol].quantity for symbol in symbols}
        current_values = {
            symbol: current_shares.get(symbol, 0) * prices[symbol] for symbol in symbols
        }

        # Calculate total portfolio value
        total_value = sum(current_values.values())
        if total_value == 0:
            raise RebalanceError("No value in portfolio to rebalance.")

        # Determine target value for each stock
        target_values = {
            symbol: self.allocation.get(symbol, 0) * total_value for symbol in symbols
        }

        # Determine shares to buy/sell for each stock
        rebalance = {}
        for symbol in symbols:
            price = prices[symbol]
            current_value = current_values.get(symbol, 0)
            target_value = target_values.get(symbol, 0)
            diff_value = target_value - current_value
            shares = diff_value / price if price > 0 else 0
            rebalance[symbol] = round(shares, 4)

        return rebalance
