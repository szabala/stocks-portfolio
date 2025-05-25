from ports.portfolio_repository_port import PortfolioRepositoryPort
from domains.stock.aggregates import Portfolio
from exceptions.infrastructure import NotFoundError


class MemoryPortfolioRepository(PortfolioRepositoryPort):
    def __init__(self):
        self._store = {}

    def save(self, portfolio_id: str, portfolio: Portfolio):
        self._store[portfolio_id] = portfolio

    def get(self, portfolio_id: str) -> Portfolio:
        portfolio = self._store.get(portfolio_id)
        if portfolio is None:
            raise NotFoundError(f"Portfolio '{portfolio_id}' not found.")
        return portfolio
