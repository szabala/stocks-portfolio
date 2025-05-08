from ports.portfolio_repository_port import PortfolioRepositoryPort
from domains.stock.aggregates import Portfolio


class MemoryPortfolioRepository(PortfolioRepositoryPort):
    def __init__(self):
        self._store = {}

    def save(self, portfolio_id: str, portfolio: Portfolio):
        self._store[portfolio_id] = portfolio

    def get(self, portfolio_id: str) -> Portfolio:
        return self._store.get(portfolio_id)
