from .entities import Stock
from typing import List
from datetime import date


class Portfolio:
    def __init__(self, stocks: List[Stock]):
        self.stocks = stocks

    def calculate_profit(self, start_date: date, end_date: date, provider):
        total_start = sum(
            s.price(start_date, provider) * s.quantity for s in self.stocks
        )
        total_end = sum(s.price(end_date, provider) * s.quantity for s in self.stocks)
        profit = total_end - total_start
        duration_years = (end_date - start_date).days / 365.25
        annualized = (
            ((total_end / total_start) ** (1 / duration_years) - 1)
            if duration_years > 0 and total_start > 0
            else 0
        )
        return {"profit": profit, "annualized_return": annualized}
