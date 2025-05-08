from domains.stock.aggregates import Portfolio
from domains.stock.entities import Stock
from ports.stock_price_port import StockPricePort
from ports.portfolio_repository_port import PortfolioRepositoryPort
import uuid


class PortfolioService:
    def __init__(
        self,
        price_provider: StockPricePort,
        repository: PortfolioRepositoryPort,
    ):
        self.price_provider = price_provider
        self.repository = repository

    def create_portfolio(self, stocks: list[Stock]):
        portfolio = Portfolio(stocks)
        portfolio_id = str(uuid.uuid4())
        self.repository.save(portfolio_id, portfolio)
        return {"portfolio_id": portfolio_id}

    def get_portfolio(self, portfolio_id: str):
        return self.repository.get(portfolio_id)

    def calculate_profit(self, portfolio_id: str, start_date: str, end_date: str):
        portfolio = self.repository.get(portfolio_id)
        if not portfolio:
            raise ValueError("Portfolio not found")
        return portfolio.calculate_profit(start_date, end_date, self.price_provider)
