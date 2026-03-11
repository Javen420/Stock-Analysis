import numpy as np
from bson import ObjectId
from datetime import datetime
from app.core.mongo import db

stocks_col = db["stocks"]
prices_col = db["stock_prices"]
analytics_col = db["analytics"]


class TechnicalsCalculator:
    """Calculates technical indicators and scores for a stock, persists to analytics collection."""

    def __init__(self, symbol: str):
        self.symbol = symbol.upper()
        self._stock = None
        self._prices = None
        self._dates = None

    def _load_stock(self) -> dict:
        if self._stock is None:
            self._stock = stocks_col.find_one({"symbol": self.symbol})
        return self._stock

    def _load_prices(self):
        if self._prices is None:
            cursor = prices_col.find(
                {"symbol": self.symbol}, {"price": 1, "date": 1}
            ).sort("date", 1)
            docs = list(cursor)
            self._prices = np.array([d["price"] for d in docs]) if docs else np.array([])
            self._dates = [d["date"] for d in docs] if docs else []

    # ── Technical Indicators ──

    def sma(self, period: int) -> float | None:
        self._load_prices()
        if len(self._prices) < period:
            return None
        return round(float(np.mean(self._prices[-period:])), 4)

    def rsi(self, period: int = 14) -> float | None:
        self._load_prices()
        if len(self._prices) < period + 1:
            return None

        deltas = np.diff(self._prices[-(period + 1):])
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)

        avg_gain = np.mean(gains)
        avg_loss = np.mean(losses)

        if avg_loss == 0:
            return 100.0
        rs = avg_gain / avg_loss
        return round(100 - (100 / (1 + rs)), 2)

    def macd(self) -> dict | None:
        self._load_prices()
        if len(self._prices) < 35:
            return None

        prices = self._prices.astype(float)

        ema12 = self._ema(prices, 12)
        ema26 = self._ema(prices, 26)
        macd_line = ema12 - ema26

        # Signal line: 9-period EMA of the MACD line
        signal = self._ema(macd_line, 9)
        histogram = macd_line[-1] - signal[-1]

        return {
            "macd": round(float(macd_line[-1]), 4),
            "signal": round(float(signal[-1]), 4),
            "histogram": round(float(histogram), 4),
        }

    @staticmethod
    def _ema(data: np.ndarray, span: int) -> np.ndarray:
        alpha = 2 / (span + 1)
        ema = np.zeros_like(data, dtype=float)
        ema[0] = data[0]
        for i in range(1, len(data)):
            ema[i] = alpha * data[i] + (1 - alpha) * ema[i - 1]
        return ema

    # ── Fundamentals (from Alpha Vantage overview already stored in stocks collection) ──

    def fundamentals(self) -> dict:
        stock = self._load_stock()
        if not stock:
            return {}

        def to_float(val):
            if val is None or val == "None" or val == "":
                return None
            try:
                return round(float(val), 4)
            except (ValueError, TypeError):
                return None

        return {
            "pe": to_float(stock.get("pe")),
            "eps": to_float(stock.get("eps")),
            "pb": to_float(stock.get("pb")),
            "fcf": to_float(stock.get("fcf")),
            "dividendYield": to_float(stock.get("dividendYield")),
            "revenueGrowth": to_float(stock.get("revenueGrowth")),
            "profitMargin": to_float(stock.get("profitMargin")),
            "debtToEquity": to_float(stock.get("debtToEquity")),
            "roe": to_float(stock.get("roe")),
            "roa": to_float(stock.get("roa")),
        }

    # ── Scoring ──

    def value_score(self) -> float:
        """0-25: Based on PE, PB, dividend yield. Lower PE/PB and higher yield = better."""
        f = self.fundamentals()
        score = 0.0
        count = 0

        pe = f.get("pe")
        if pe is not None and pe > 0:
            # PE < 15 = full marks, PE > 30 = 0
            score += max(0, min(1 - (pe - 15) / 15, 1)) * 10
            count += 1

        pb = f.get("pb")
        if pb is not None and pb > 0:
            # PB < 1.5 = full marks, PB > 5 = 0
            score += max(0, min(1 - (pb - 1.5) / 3.5, 1)) * 8
            count += 1

        dy = f.get("dividendYield")
        if dy is not None:
            # Yield > 4% = full marks, 0% = 0
            score += min(dy / 0.04, 1) * 7
            count += 1

        if count == 0:
            return 12.5  # neutral
        # Scale to the max possible given available metrics
        max_possible = count / 3 * 25
        return round(score / max_possible * 25 if max_possible > 0 else 12.5, 2)

    def growth_score(self) -> float:
        """0-25: Based on EPS, revenue growth, profit margin, ROE."""
        f = self.fundamentals()
        score = 0.0
        count = 0

        rg = f.get("revenueGrowth")
        if rg is not None:
            # 20%+ growth = full marks, negative = 0
            score += max(0, min(rg / 0.2, 1)) * 8
            count += 1

        pm = f.get("profitMargin")
        if pm is not None:
            # 20%+ margin = full marks, 0% = 0
            score += max(0, min(pm / 0.2, 1)) * 8
            count += 1

        roe = f.get("roe")
        if roe is not None:
            # 20%+ ROE = full marks, 0% = 0
            score += max(0, min(roe / 0.2, 1)) * 9
            count += 1

        if count == 0:
            return 12.5
        max_possible = count / 3 * 25
        return round(score / max_possible * 25 if max_possible > 0 else 12.5, 2)

    def momentum_score(self) -> float:
        """0-25: Based on RSI, MACD, SMA alignment."""
        self._load_prices()
        score = 0.0
        count = 0

        rsi_val = self.rsi()
        if rsi_val is not None:
            # RSI 50 = neutral(mid), 30-70 is healthy range
            # Best score around 55-65 (bullish but not overbought)
            if 40 <= rsi_val <= 70:
                score += ((rsi_val - 40) / 30) * 8
            elif rsi_val > 70:
                score += max(0, 8 - (rsi_val - 70) / 10 * 8)
            count += 1

        macd_data = self.macd()
        if macd_data is not None:
            # Positive histogram = bullish momentum
            hist = macd_data["histogram"]
            score += min(max(hist / 2, 0), 1) * 8
            count += 1

        sma20 = self.sma(20)
        sma50 = self.sma(50)
        if sma20 is not None and sma50 is not None and sma50 > 0:
            ratio = sma20 / sma50
            # ratio > 1 = uptrend
            score += max(0, min((ratio - 0.95) / 0.1, 1)) * 9
            count += 1

        if count == 0:
            return 12.5
        max_possible = count / 3 * 25
        return round(score / max_possible * 25 if max_possible > 0 else 12.5, 2)

    def overall_score(self) -> float:
        """0-100: Combined value + growth + momentum + stock_scorer trend/vol/consistency."""
        from app.services.stock_scorer import StockScorer

        self._load_prices()
        scorer = StockScorer(self.symbol, prices=list(self._prices))
        base = scorer.combined_score()["combined_score"]  # 0-100

        val = self.value_score()      # 0-25
        growth = self.growth_score()  # 0-25
        momentum = self.momentum_score()  # 0-25

        # Blend: 25% base stock score + 25% value + 25% growth + 25% momentum
        blended = (base * 0.25) + val + growth + momentum
        return round(min(blended, 100), 2)

    # ── Compute & Persist ──

    def compute(self) -> dict:
        """Compute all technicals, fundamentals, and scores. Returns the full document."""
        stock = self._load_stock()
        if not stock:
            return None

        stock_id = stock["_id"]

        sma20 = self.sma(20)
        sma50 = self.sma(50)
        sma200 = self.sma(200)
        rsi_val = self.rsi()
        macd_data = self.macd()

        doc = {
            "stockId": stock_id,
            "fundamentals": self.fundamentals(),
            "technicals": {
                "rsi": rsi_val,
                "macd": macd_data,
                "sma20": sma20,
                "sma50": sma50,
                "sma200": sma200,
            },
            "scoring": {
                "valueScore": self.value_score(),
                "growthScore": self.growth_score(),
                "momentumScore": self.momentum_score(),
                "overallScore": self.overall_score(),
            },
            "lastUpdated": datetime.utcnow(),
        }

        analytics_col.update_one(
            {"stockId": stock_id},
            {"$set": doc},
            upsert=True,
        )

        return doc

    def get_cached(self) -> dict | None:
        """Return cached analytics doc if it exists."""
        stock = self._load_stock()
        if not stock:
            return None
        return analytics_col.find_one({"stockId": stock["_id"]})
