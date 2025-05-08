from fastapi import APIRouter, HTTPException
from application.portfolio_service import PortfolioService
from routers.entities import PortfolioInput, ProfitInput
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
    return portfolio_service.create_portfolio(stocks)


@router.get("/{portfolio_id}")
def get_portfolio(portfolio_id: str):
    portfolio = portfolio_service.get_portfolio(portfolio_id)
    if not portfolio:
        raise HTTPException(status_code=404, detail="Portfolio not found")
    return portfolio


@router.post("/{portfolio_id}/profit")
def calculate_profit(portfolio_id: str, data: ProfitInput):
    return portfolio_service.calculate_profit(
        portfolio_id, data.start_date, data.end_date
    )
