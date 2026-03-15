# app/api/stocks.py
import re
from fastapi import APIRouter, HTTPException
from app.core.mongo import db
from app.services.stock_api import fetch_and_store_stock
from app.services.technicals import TechnicalsCalculator
from app.services.cache import is_stale

router = APIRouter()

prices_collection = db["stock_prices"]
stocks_collection = db["stocks"]

SYMBOL_PATTERN = re.compile(r"^[A-Za-z]{1,5}$")


def _validate_symbol(symbol: str) -> str:
    if not SYMBOL_PATTERN.match(symbol):
        raise HTTPException(status_code=400, detail="Invalid ticker symbol")
    return symbol.upper()


@router.get("/{symbol}")
def get_stock(symbol: str):
    symbol = _validate_symbol(symbol)

    # 1️⃣ Get stock info, auto-fetch from Alpha Vantage if not in DB
    stock = stocks_collection.find_one({"symbol": symbol})
    if not stock:
        try:
            fetch_and_store_stock(symbol)
        except ValueError:
            raise HTTPException(status_code=404, detail=f"Ticker '{symbol}' not found")
        stock = stocks_collection.find_one({"symbol": symbol})

    # 2️⃣ Get price history from Mongo
    prices_cursor = prices_collection.find({"symbol": symbol}).sort("date", -1)
    prices = [
        {"date": p["date"].strftime("%Y-%m-%d") if hasattr(p["date"], "strftime") else p["date"], "price": p["price"]}
        for p in prices_cursor
    ]

    # 3️⃣ Return both stock info and prices
    return {
        "symbol": symbol,
        "name": stock["name"],
        "sector": stock.get("sector"),
        "industry": stock.get("industry"),
        "exchange": stock.get("exchange"),
        "description": stock.get("description"),
        "prices": prices
    }


@router.get("/{symbol}/technicals")
def get_technicals(symbol: str):
    symbol = _validate_symbol(symbol)

    stock = stocks_collection.find_one({"symbol": symbol})
    if not stock:
        raise HTTPException(status_code=404, detail=f"Ticker '{symbol}' not found")

    calc = TechnicalsCalculator(symbol)

    # Return cached data if fresh, otherwise recompute
    cached = calc.get_cached()
    if cached and not is_stale(cached.get("lastUpdated")):
        cached.pop("_id", None)
        cached.pop("stockId", None)
        return {"symbol": symbol, **_serialize(cached)}

    result = calc.compute()
    if not result:
        raise HTTPException(status_code=500, detail="Failed to compute technicals")

    result.pop("_id", None)
    result.pop("stockId", None)
    return {"symbol": symbol, **_serialize(result)}


def _serialize(doc: dict) -> dict:
    """Convert ObjectId/datetime fields to JSON-safe types."""
    from bson import ObjectId
    from datetime import datetime

    out = {}
    for k, v in doc.items():
        if isinstance(v, ObjectId):
            out[k] = str(v)
        elif isinstance(v, datetime):
            out[k] = v.isoformat()
        elif isinstance(v, dict):
            out[k] = _serialize(v)
        else:
            out[k] = v
    return out
