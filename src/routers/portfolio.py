from fastapi import APIRouter, HTTPException
from application.portfolio_service import PortfolioService
from exceptions.domain import RebalanceError
from exceptions.infrastructure import NotFoundError
from routers.entities import PortfolioInput, PortfolioOutput, RebalanceOutput
from infrastructure.memory_portfolio_repository import MemoryPortfolioRepository
from infrastructure.stock_price_provider import DummyStockPriceProvider

router = APIRouter(prefix="/portfolio")

portfolio_repository = MemoryPortfolioRepository()
price_provider = DummyStockPriceProvider()
portfolio_service = PortfolioService(
    repository=portfolio_repository, price_provider=price_provider
)


@router.post(
    "/",
    response_model=PortfolioOutput,
    description="Create a new portfolio with the specified stocks and target allocation.",
)
def create_portfolio(data: PortfolioInput):
    stocks = data.to_domain()
    allocation = data.allocation
    portfolio_id, portfolio = portfolio_service.create_portfolio(stocks, allocation)
    value = portfolio.value(portfolio_service.price_provider)
    return PortfolioOutput.from_domain(portfolio_id, portfolio, value)


@router.get(
    "/{portfolio_id}",
    response_model=PortfolioOutput,
    description="Retrieve a portfolio by its ID, including its current value.",
)
def get_portfolio(portfolio_id: str):
    try:
        portfolio_id, portfolio = portfolio_service.get_portfolio(portfolio_id)
        value = portfolio.value(portfolio_service.price_provider)
        return PortfolioOutput.from_domain(portfolio_id, portfolio, value)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get(
    "/{portfolio_id}/rebalance",
    response_model=RebalanceOutput,
    description="Retrieve which stocks should be sold and bought to align the portfolio with the target allocation.",
)
def rebalance(portfolio_id: str):
    try:
        rebalance_dict = portfolio_service.rebalance_portfolio(portfolio_id)
        return RebalanceOutput.from_domain(rebalance_dict)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RebalanceError as e:
        raise HTTPException(status_code=400, detail=str(e))
