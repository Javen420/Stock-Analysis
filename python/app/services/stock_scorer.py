import numpy as np
from app.core.mongo import db

prices_col = db["stock_prices"]


class StockScorer:
    """Scores an individual stock (0-100) based on price history metrics."""

    def __init__(self, symbol: str, prices: list[float] = None):
        self.symbol = symbol.upper()
        if prices is not None:
            self.prices = np.array(prices)
        else:
            self.prices = self._load_prices()

    def _load_prices(self) -> np.ndarray:
        cursor = prices_col.find(
            {"symbol": self.symbol}, {"price": 1, "date": 1}
        ).sort("date", 1)
        vals = [doc["price"] for doc in cursor]
        return np.array(vals) if vals else np.array([])

    def trend_score(self) -> float:
        """0-40: Compare short-term SMA vs long-term SMA to gauge momentum."""
        if len(self.prices) < 50:
            return 20  # neutral if not enough data

        sma_20 = np.mean(self.prices[-20:])
        sma_50 = np.mean(self.prices[-50:])

        if sma_50 == 0:
            return 20

        ratio = sma_20 / sma_50
        # ratio > 1 means uptrend, < 1 means downtrend
        # Map ratio 0.9 -> 0, 1.0 -> 20, 1.1 -> 40
        score = max(0, min((ratio - 0.9) / 0.2, 1)) * 40
        return round(score, 2)

    def volatility_score(self) -> float:
        """0-30: Lower volatility = higher score."""
        if len(self.prices) < 10:
            return 15

        returns = np.diff(self.prices) / self.prices[:-1]
        vol = np.std(returns)

        # Annualized volatility
        annual_vol = vol * np.sqrt(252)
        # Map: 0% vol -> 30, 60%+ vol -> 0
        score = max(0, min(1 - annual_vol / 0.6, 1)) * 30
        return round(score, 2)

    def consistency_score(self) -> float:
        """0-30: Percentage of positive return days over recent history."""
        if len(self.prices) < 10:
            return 15

        returns = np.diff(self.prices) / self.prices[:-1]
        positive_ratio = np.sum(returns > 0) / len(returns)
        # Map: 40% positive -> 0, 60%+ positive -> 30
        score = max(0, min((positive_ratio - 0.4) / 0.2, 1)) * 30
        return round(score, 2)

    def combined_score(self) -> dict:
        """Returns combined score dict expected by PortfolioScorer."""
        if len(self.prices) < 2:
            return {"combined_score": 0}

        total = self.trend_score() + self.volatility_score() + self.consistency_score()
        return {"combined_score": round(total, 2)}
