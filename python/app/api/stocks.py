# app/api/stocks.py
from fastapi import APIRouter, HTTPException
from pymongo import MongoClient
from typing import List

router = APIRouter()

# Mongo connection
client = MongoClient("mongodb://localhost:27017")
db = client["stock_db"]
prices_collection = db["stock_prices"]
stocks_collection = db["stocks"]

@router.get("/{symbol}")
def get_stock(symbol: str):
    symbol = symbol.upper()

    # 1️⃣ Get stock info
    stock = stocks_collection.find_one({"symbol": symbol})
    if not stock:
        raise HTTPException(status_code=404, detail=f"Ticker '{symbol}' not found")

    # 2️⃣ Get price history from Mongo
    prices_cursor = prices_collection.find({"symbol": symbol}).sort("date", -1)
    prices = [{"date": p["date"], "price": p["price"]} for p in prices_cursor]

    # 3️⃣ Return both stock info and prices
    return {
        "symbol": symbol,
        "name": stock["name"],
        "prices": prices
    }
