from pydantic import BaseModel, validator
from typing import List
from domains.stock.entities import Stock
from datetime import date, datetime


class StockInput(BaseModel):
    symbol: str
    quantity: float

    def to_domain(self) -> Stock:
        return Stock(symbol=self.symbol, quantity=self.quantity)


class PortfolioInput(BaseModel):
    stocks: List[StockInput]

    def to_domain(self) -> List[Stock]:
        return [stock.to_domain() for stock in self.stocks]


class ProfitInput(BaseModel):
    start_date: date
    end_date: date

    @validator("start_date", "end_date", pre=True)
    def parse_date(cls, value):
        if isinstance(value, date):
            return value
        for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%d/%m/%Y"):
            try:
                return datetime.strptime(value, fmt).date()
            except ValueError:
                continue
        raise ValueError(f"Invalid date format: {value}")
