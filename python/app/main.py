from fastapi import FastAPI
from app.api import stocks, grades

app = FastAPI()

app.include_router(stocks.router, prefix="/stocks")
app.include_router(grades.router, prefix="/grades")


