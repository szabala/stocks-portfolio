from pydantic import BaseModel, validator, Field
from typing import List, Dict, TypeAlias
from domains.stock.entities import Stock

Allocation: TypeAlias = Dict[str, float]


class StockInput(BaseModel):
    symbol: str = Field(..., example="AAPL", description="Stock symbol")
    quantity: float = Field(..., example=10.0, description="Number of shares")

    def to_domain(self) -> Stock:
        return Stock(symbol=self.symbol, quantity=self.quantity)


class StockOutput(BaseModel):
    symbol: str = Field(..., example="AAPL", description="Stock symbol")
    quantity: float = Field(..., example=10.0, description="Number of shares")

    @classmethod
    def from_domain(cls, stock: Stock) -> "StockOutput":
        return cls(symbol=stock.symbol, quantity=stock.quantity)


class PortfolioInput(BaseModel):
    stocks: List[StockInput] = Field(
        ...,
        example=[{"symbol": "AAPL", "quantity": 10}, {"symbol": "GOOG", "quantity": 5}],
        description="List of stocks in the portfolio",
    )
    allocation: Allocation = Field(
        description="Mapping of stock symbol to allocation percentage (values should sum to 1.0)",
        example={"AAPL": 0.5, "GOOG": 0.3, "MSFT": 0.2},
    )

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


class PortfolioOutput(BaseModel):
    id: str = Field(
        ..., description="Unique portfolio identifier"
    )
    stocks: List[StockOutput] = Field(
        ...,
        example=[{"symbol": "AAPL", "quantity": 10}, {"symbol": "GOOG", "quantity": 5}],
        description="List of stocks in the portfolio",
    )
    allocation: Allocation = Field(
        ...,
        description="Mapping of stock symbol to allocation percentage (values sum to 1.0)",
        example={"AAPL": 0.5, "GOOG": 0.3, "MSFT": 0.2},
    )
    value: float = Field(
        ..., example=15000.0, description="Total portfolio value in USD"
    )

    @classmethod
    def from_domain(
        cls, portfolio_id: str, portfolio, value: float
    ) -> "PortfolioOutput":
        return cls(
            id=portfolio_id,
            stocks=[StockOutput.from_domain(s) for s in portfolio.stocks],
            allocation=portfolio.allocation,
            value=value,
        )


class RebalanceAction(BaseModel):
    symbol: str = Field(..., example="AAPL", description="Stock symbol to buy or sell")
    quantity: float = Field(
        ..., example=2.5, description="Number of shares to buy or sell"
    )


class RebalanceOutput(BaseModel):
    buy: List[RebalanceAction] = Field(
        ...,
        example=[{"symbol": "AAPL", "quantity": 2.5}],
        description="List of stocks to buy with quantities",
    )
    sell: List[RebalanceAction] = Field(
        ...,
        example=[{"symbol": "GOOG", "quantity": 1.0}],
        description="List of stocks to sell with quantities",
    )

    @classmethod
    def from_domain(cls, rebalance: Dict[str, float]) -> "RebalanceOutput":
        buy, sell = [], []
        for symbol, quantity in rebalance.items():
            if quantity > 0:
                buy.append(RebalanceAction(symbol=symbol, quantity=abs(quantity)))
            elif quantity < 0:
                sell.append(RebalanceAction(symbol=symbol, quantity=abs(quantity)))
        return cls(buy=buy, sell=sell)
