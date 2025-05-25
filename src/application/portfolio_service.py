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

    def create_portfolio(self, stocks: list[Stock], allocation: dict = None):
        portfolio = Portfolio(stocks, allocation)
        portfolio_id = str(uuid.uuid4())
        self.repository.save(portfolio_id, portfolio)
        return portfolio_id, portfolio

    def get_portfolio(self, portfolio_id: str):
        portfolio = self.repository.get(portfolio_id)
        return portfolio_id, portfolio

    def rebalance_portfolio(self, portfolio_id: str):
        return self.repository.get(portfolio_id).rebalance(self.price_provider)
