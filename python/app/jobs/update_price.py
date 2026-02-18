"""Seed or refresh stock data in MongoDB using Alpha Vantage.

Usage:
    # Seed specific tickers
    python -m app.jobs.update_price AAPL MSFT GOOGL

    # Refresh all stocks already in the DB
    python -m app.jobs.update_price --all

Notes:
    - Alpha Vantage free tier: 25 requests/day, ~12 requests/min
    - Each stock costs 2 requests (overview + prices)
    - A 12-second delay between stocks keeps you under the per-minute cap
    - Set ALPHA_VANTAGE_KEY in your .env before running
"""

import sys
import time

from app.core.mongo import db
from app.services.stock_api import fetch_and_store_stock

DELAY_BETWEEN_STOCKS = 13  # seconds — safe for AV free tier (~12 req/min)


def main():
    args = sys.argv[1:]

    if not args:
        print(__doc__)
        sys.exit(1)

    if args == ["--all"]:
        stocks = list(db["stocks"].find({}, {"symbol": 1}))
        symbols = [s["symbol"] for s in stocks]
        if not symbols:
            print("No stocks in database yet. Seed with: python -m app.jobs.update_price AAPL MSFT GOOGL")
            sys.exit(1)
    else:
        symbols = [s.upper() for s in args]

    print(f"Fetching {len(symbols)} stock(s): {', '.join(symbols)}")
    print(f"(Each stock = 2 API calls; {DELAY_BETWEEN_STOCKS}s delay between stocks)\n")

    for i, symbol in enumerate(symbols):
        try:
            count = fetch_and_store_stock(symbol)
            print(f"✅ {symbol}: stored {count} price records")
        except Exception as e:
            print(f"❌ {symbol}: {e}")

        if i < len(symbols) - 1:
            time.sleep(DELAY_BETWEEN_STOCKS)

    print("\nDone.")


if __name__ == "__main__":
    main()
