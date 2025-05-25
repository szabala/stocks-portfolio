from fastapi import APIRouter, HTTPException
from application.portfolio_service import PortfolioService
from exceptions.domain import RebalanceError
from exceptions.infrastructure import NotFoundError
from routers.entities import PortfolioInput, RebalanceOutput
from infrastructure.memory_portfolio_repository import MemoryPortfolioRepository
from infrastructure.stock_price_provider import DummyStockPriceProvider

router = APIRouter(prefix="/portfolio")

portfolio_repository = MemoryPortfolioRepository()
price_provider = DummyStockPriceProvider()
portfolio_service = PortfolioService(
    repository=portfolio_repository, price_provider=price_provider
)


@router.post("/")
def create_portfolio(data: PortfolioInput):
    stocks = data.to_domain()
    allocation = data.allocation
    return portfolio_service.create_portfolio(stocks, allocation)


@router.get("/{portfolio_id}")
def get_portfolio(portfolio_id: str):
    try:
        return portfolio_service.get_portfolio(portfolio_id)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{portfolio_id}/rebalance", response_model=RebalanceOutput)
def rebalance(portfolio_id: str):
    try:
        rebalance_dict = portfolio_service.rebalance_portfolio(portfolio_id)
        return RebalanceOutput.from_domain(rebalance_dict)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except RebalanceError as e:
        raise HTTPException(status_code=400, detail=str(e))