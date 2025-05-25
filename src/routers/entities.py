from pydantic import BaseModel, validator
from typing import List, Dict, Optional
from domains.stock.entities import Stock


class StockInput(BaseModel):
    symbol: str
    quantity: float

    def to_domain(self) -> Stock:
        return Stock(symbol=self.symbol, quantity=self.quantity)


class PortfolioInput(BaseModel):
    stocks: List[StockInput]
    allocation: Dict[str, float] = None

    def to_domain(self) -> List[Stock]:
        return [stock.to_domain() for stock in self.stocks]

    @validator("allocation")
    def validate_allocation(cls, v):
        if v is not None:
            total = sum(v.values())
            if total != 1.0:
                raise ValueError("Allocation must sum to 1.0")
        return v

    @validator("stocks")
    def validate_stocks(cls, v):
        symbols = set()
        for stock in v:
            if stock.quantity <= 0:
                raise ValueError("Stock quantity must be positive")
            if stock.symbol in symbols:
                raise ValueError(f"Duplicate stock symbol found: {stock.symbol}")
            symbols.add(stock.symbol)
        return v


class RebalanceAction(BaseModel):
    symbol: str
    quantity: float


class RebalanceOutput(BaseModel):
    buy: List[RebalanceAction]
    sell: List[RebalanceAction]

    @classmethod
    def from_domain(cls, rebalance: Dict[str, float]) -> "RebalanceOutput":
        buy, sell = [], []
        for symbol, quantity in rebalance.items():
            if quantity > 0:
                buy.append(RebalanceAction(symbol=symbol, quantity=abs(quantity)))
            elif quantity < 0:
                sell.append(RebalanceAction(symbol=symbol, quantity=abs(quantity)))
        return cls(buy=buy, sell=sell)
