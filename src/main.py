from fastapi import FastAPI
from src.routers import portfolio

app = FastAPI()
app.include_router(portfolio.router)
