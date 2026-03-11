import os
from datetime import datetime
import requests
from dotenv import load_dotenv

load_dotenv()
from app.core.mongo import db

AV_API_KEY = os.getenv("ALPHA_VANTAGE_KEY", "demo")
AV_BASE = "https://www.alphavantage.co/query"

stocks_col = db["stocks"]
prices_col = db["stock_prices"]


def fetch_and_store_stock(symbol: str) -> int:
    """Fetch company info + price history from Alpha Vantage and upsert into MongoDB.
    Returns the number of price records stored.
    Raises ValueError if the symbol is not found.
    """
    symbol = symbol.upper()

    # 1. Company overview
    overview_resp = requests.get(AV_BASE, params={
        "function": "OVERVIEW",
        "symbol": symbol,
        "apikey": AV_API_KEY,
    }, timeout=15)
    overview_resp.raise_for_status()
    overview = overview_resp.json()

    if not overview.get("Symbol"):
        raise ValueError(f"No overview data found for '{symbol}'. Check the ticker or your API key.")

    def _safe_float(val):
        if val is None or val == "None" or val == "" or val == "-":
            return None
        try:
            return float(val)
        except (ValueError, TypeError):
            return None

    stocks_col.update_one(
        {"symbol": symbol},
        {"$set": {
            "symbol": symbol,
            "name": overview.get("Name", symbol),
            "exchange": overview.get("Exchange"),
            "sector": overview.get("Sector"),
            "industry": overview.get("Industry"),
            "description": overview.get("Description"),
            "pe": _safe_float(overview.get("PERatio")),
            "eps": _safe_float(overview.get("EPS")),
            "pb": _safe_float(overview.get("PriceToBookRatio")),
            "fcf": _safe_float(overview.get("OperatingCashflow")),
            "dividendYield": _safe_float(overview.get("DividendYield")),
            "revenueGrowth": _safe_float(overview.get("QuarterlyRevenueGrowthYOY")),
            "profitMargin": _safe_float(overview.get("ProfitMargin")),
            "debtToEquity": _safe_float(overview.get("DebtToEquityRatio")),
            "roe": _safe_float(overview.get("ReturnOnEquityTTM")),
            "roa": _safe_float(overview.get("ReturnOnAssetsTTM")),
        }},
        upsert=True,
    )

    # 2. Daily price history (last ~100 trading days)
    prices_resp = requests.get(AV_BASE, params={
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "compact",
        "apikey": AV_API_KEY,
    }, timeout=15)
    prices_resp.raise_for_status()
    prices_data = prices_resp.json()

    time_series = prices_data.get("Time Series (Daily)", {})
    if not time_series:
        raise ValueError(f"No price data returned for '{symbol}'. May be a rate-limit issue.")

    for date_str, ohlcv in time_series.items():
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        prices_col.update_one(
            {"symbol": symbol, "date": date_obj},
            {"$set": {
                "symbol": symbol,
                "date": date_obj,
                "price": float(ohlcv["4. close"]),
                "open": float(ohlcv["1. open"]),
                "high": float(ohlcv["2. high"]),
                "low": float(ohlcv["3. low"]),
                "volume": int(ohlcv["5. volume"]),
            }},
            upsert=True,
        )

    return len(time_series)
