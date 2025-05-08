from abc import ABC, abstractmethod
from domains.stock.aggregates import Portfolio


class PortfolioRepositoryPort(ABC):
    @abstractmethod
    def save(self, portfolio_id: str, portfolio: Portfolio):
        pass

    @abstractmethod
    def get(self, portfolio_id: str) -> Portfolio:
        pass
