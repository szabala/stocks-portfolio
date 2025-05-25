import pytest
from domains.stock.aggregates import Portfolio
from domains.stock.entities import Stock
from exceptions.domain import RebalanceError


class DummyPriceProvider:
    def __init__(self, prices):
        self.prices = prices

    def get_price(self, symbol, date=None):
        return self.prices[symbol]


@pytest.fixture
def stocks():
    return [
        Stock(symbol="AAPL", quantity=10),
        Stock(symbol="GOOG", quantity=5),
    ]


@pytest.fixture
def allocation():
    return {"AAPL": 0.6, "GOOG": 0.4}


@pytest.fixture
def price_provider():
    provider = DummyPriceProvider({"AAPL": 100, "GOOG": 200})
    return provider


def test_value(stocks, allocation, price_provider, monkeypatch):
    monkeypatch.setattr(
        "domains.stock.entities.Stock.current_price",
        lambda self, provider: provider.get_price(self.symbol),
    )
    portfolio = Portfolio(stocks, allocation)
    assert portfolio.value(price_provider) == 2000


def test_rebalance(stocks, allocation, price_provider, monkeypatch):
    monkeypatch.setattr(
        "domains.stock.entities.Stock.current_price",
        lambda self, provider: provider.get_price(self.symbol),
    )
    portfolio = Portfolio(stocks, allocation)
    result = portfolio.rebalance(price_provider)
    assert set(result.keys()) == {"AAPL", "GOOG"}
    # Assert that the rebalance is correct to a margin of error
    assert abs(sum(result[s] * price_provider.get_price(s) for s in result)) < 1e-6


def test_rebalance_no_allocation(stocks, price_provider, monkeypatch):
    monkeypatch.setattr(
        "domains.stock.entities.Stock.current_price",
        lambda self, provider: provider.get_price(self.symbol),
    )
    portfolio = Portfolio(stocks, {})
    with pytest.raises(RebalanceError):
        portfolio.rebalance(price_provider)


def test_rebalance_zero_value(monkeypatch):
    stocks = [Stock(symbol="AAPL", quantity=0)]
    allocation = {"AAPL": 1.0}
    provider = DummyPriceProvider({"AAPL": 100})
    monkeypatch.setattr(
        "domains.stock.entities.Stock.current_price",
        lambda self, provider: provider.get_price(self.symbol),
    )
    portfolio = Portfolio(stocks, allocation)
    with pytest.raises(RebalanceError):
        portfolio.rebalance(provider)
