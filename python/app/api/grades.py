from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.mongo import db
from app.services.grading import PortfolioScorer
from app.services.stock_scorer import StockScorer
from app.services.stock_api import fetch_and_store_stock

router = APIRouter()

prices_col = db["stock_prices"]
stocks_col = db["stocks"]


class Holding(BaseModel):
    symbol: str
    shares: float
    averageCost: float


class GradeRequest(BaseModel):
    holdings: list[Holding]


def _ensure_stock_data(symbol: str):
    """Fetch stock data from Alpha Vantage if not already in DB."""
    if not stocks_col.find_one({"symbol": symbol}):
        try:
            fetch_and_store_stock(symbol)
        except ValueError as e:
            print(f"[WARN] Could not fetch stock data for {symbol}: {e}")
        except Exception as e:
            print(f"[ERROR] Unexpected error fetching {symbol}: {e}")


def _get_latest_price(symbol: str) -> float | None:
    doc = prices_col.find_one({"symbol": symbol}, sort=[("date", -1)])
    return doc["price"] if doc else None


def _get_prices_sorted(symbol: str) -> list[float]:
    cursor = prices_col.find({"symbol": symbol}).sort("date", 1)
    return [doc["price"] for doc in cursor]


def _build_portfolio_values(holdings: list[Holding]) -> list[float]:
    """Build daily portfolio value series from overlapping price dates."""
    # Collect date->price for each holding
    date_prices = {}
    for h in holdings:
        cursor = prices_col.find({"symbol": h.symbol.upper()}).sort("date", 1)
        for doc in cursor:
            date = doc["date"]
            if date not in date_prices:
                date_prices[date] = {}
            date_prices[date][h.symbol.upper()] = doc["price"]

    if not date_prices:
        return []

    symbols = [h.symbol.upper() for h in holdings]
    shares_map = {h.symbol.upper(): h.shares for h in holdings}

    # Only use dates where all holdings have data
    sorted_dates = sorted(date_prices.keys())
    values = []
    for date in sorted_dates:
        day_prices = date_prices[date]
        if all(s in day_prices for s in symbols):
            total = sum(day_prices[s] * shares_map[s] for s in symbols)
            values.append(total)

    return values


@router.post("")
def get_portfolio_grade(req: GradeRequest):
    if not req.holdings:
        raise HTTPException(status_code=400, detail="No holdings provided")

    # Ensure all stocks have data
    for h in req.holdings:
        _ensure_stock_data(h.symbol.upper())

    # Build stock scorers and weights
    stock_scorers = {}
    total_value = 0
    holding_values = {}

    for h in req.holdings:
        symbol = h.symbol.upper()
        price = _get_latest_price(symbol)
        if price is None:
            continue
        market_value = price * h.shares
        holding_values[symbol] = market_value
        total_value += market_value
        stock_scorers[symbol] = StockScorer(symbol)

    if not stock_scorers or total_value == 0:
        raise HTTPException(status_code=400, detail="Could not calculate scores — no price data found")

    weights = {s: v / total_value for s, v in holding_values.items()}

    # Get sectors
    sectors = {}
    for symbol in stock_scorers:
        stock = stocks_col.find_one({"symbol": symbol})
        if stock and stock.get("sector"):
            sectors[symbol] = stock["sector"]

    # Build portfolio value history
    portfolio_values = _build_portfolio_values(req.holdings)
    if len(portfolio_values) < 2:
        portfolio_values = [total_value, total_value]  # fallback

    scorer = PortfolioScorer(stock_scorers, weights, portfolio_values, sectors)
    return scorer.total_score()


@router.post("/analysis")
def get_portfolio_analysis(req: GradeRequest):
    if not req.holdings:
        raise HTTPException(status_code=400, detail="No holdings provided")

    # Ensure all stocks have data
    for h in req.holdings:
        _ensure_stock_data(h.symbol.upper())

    holdings_detail = []
    total_value = 0
    total_cost = 0
    sector_values = {}
    stock_scorers = {}
    holding_values = {}

    for h in req.holdings:
        symbol = h.symbol.upper()
        price = _get_latest_price(symbol)
        if price is None:
            continue

        market_value = price * h.shares
        cost_basis = h.averageCost * h.shares
        pnl = market_value - cost_basis
        pnl_pct = ((price - h.averageCost) / h.averageCost * 100) if h.averageCost > 0 else 0

        stock_info = stocks_col.find_one({"symbol": symbol})
        sector = (stock_info.get("sector") if stock_info else None) or "Unknown"
        name = (stock_info.get("name") if stock_info else None) or symbol

        holdings_detail.append({
            "symbol": symbol,
            "name": name,
            "sector": sector,
            "shares": h.shares,
            "averageCost": round(h.averageCost, 2),
            "currentPrice": round(price, 2),
            "marketValue": round(market_value, 2),
            "costBasis": round(cost_basis, 2),
            "pnl": round(pnl, 2),
            "pnlPercent": round(pnl_pct, 2),
        })

        total_value += market_value
        total_cost += cost_basis
        sector_values[sector] = sector_values.get(sector, 0) + market_value
        holding_values[symbol] = market_value
        stock_scorers[symbol] = StockScorer(symbol)

    if not holdings_detail:
        raise HTTPException(status_code=400, detail="No price data found for any holdings")

    # Add allocation % to each holding
    for h in holdings_detail:
        h["allocation"] = round(h["marketValue"] / total_value * 100, 2) if total_value > 0 else 0

    # Sector breakdown
    sector_breakdown = [
        {"sector": s, "value": round(v, 2), "percent": round(v / total_value * 100, 2)}
        for s, v in sorted(sector_values.items(), key=lambda x: -x[1])
    ]

    # Portfolio grade
    weights = {s: v / total_value for s, v in holding_values.items()}
    sectors = {h["symbol"]: h["sector"] for h in holdings_detail}
    portfolio_values = _build_portfolio_values(req.holdings)
    if len(portfolio_values) < 2:
        portfolio_values = [total_value, total_value]

    scorer = PortfolioScorer(stock_scorers, weights, portfolio_values, sectors)
    grade = scorer.total_score()

    total_pnl = total_value - total_cost
    total_pnl_pct = ((total_value - total_cost) / total_cost * 100) if total_cost > 0 else 0

    return {
        "summary": {
            "totalValue": round(total_value, 2),
            "totalCost": round(total_cost, 2),
            "totalPnl": round(total_pnl, 2),
            "totalPnlPercent": round(total_pnl_pct, 2),
            "holdingsCount": len(holdings_detail),
        },
        "holdings": holdings_detail,
        "sectorBreakdown": sector_breakdown,
        "grade": grade,
    }
