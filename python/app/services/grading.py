import numpy as np

class PortfolioScorer:
    def __init__(self, stock_scorers: dict, weights: dict, portfolio_values: list, sectors: dict = None):
        """
        stock_scorers: { 'AAPL': StockScorer(...), 'MSFT': StockScorer(...), ... }
        weights:       { 'AAPL': 0.25, 'MSFT': 0.15, ... }  # must sum to 1
        portfolio_values: list of total portfolio value over time
        sectors:       { 'AAPL': 'Tech', 'MSFT': 'Tech', 'JNJ': 'Healthcare', ... }
        """

        self.stock_scorers = stock_scorers
        self.weights = weights
        self.values = np.array(portfolio_values)
        self.sectors = sectors or {}

    # -----------------------------------------------------------
    # 1. Weighted Stock Score (0–50)
    # -----------------------------------------------------------
    def weighted_stock_score(self):
        score = 0
        for ticker, scorer in self.stock_scorers.items():
            w = self.weights.get(ticker, 0)
            stock_score = scorer.combined_score()['combined_score']  # 0–100
            score += w * stock_score
        return round(score * 0.5, 2)    # normalize to 0–50

    # -----------------------------------------------------------
    # 2. Portfolio Sharpe Ratio (converted to 0–25)
    # -----------------------------------------------------------
    def portfolio_sharpe(self, risk_free_rate=0.04):
        returns = np.diff(self.values) / self.values[:-1]

        if len(returns) < 2:
            return 0

        avg_daily = np.mean(returns)
        annual_return = (1 + avg_daily)**252 - 1

        volatility = np.std(returns) * np.sqrt(252)
        if volatility == 0:
            return 0

        sharpe = (annual_return - risk_free_rate) / volatility

        # Convert Sharpe to 0–25 points
        # Sharpe 0 → 0 pts, Sharpe 2+ → 25 pts
        score = max(0, min(sharpe / 2, 1)) * 25
        return round(score, 2)

    # -----------------------------------------------------------
    # 3. Diversification Score (0–15)
    # -----------------------------------------------------------
    def diversification_score(self):
        if not self.sectors:
            return 5  # minimal score

        weights_by_sector = {}
        for ticker, sector in self.sectors.items():
            weights_by_sector[sector] = weights_by_sector.get(sector, 0) + self.weights.get(ticker, 0)

        num_sectors = len(weights_by_sector)

        # Sector count scoring
        sector_score = min(num_sectors / 8, 1) * 10  # up to 10 points

        # Concentration penalty: penalize if one sector > 40%
        max_sector_weight = max(weights_by_sector.values())
        concentration_penalty = max(0, 1 - ((max_sector_weight - 0.4) * 2))
        concentration_score = max(0, min(concentration_penalty, 1)) * 5  # up to 5 pts

        return round(sector_score + concentration_score, 2)  # 0–15

    # -----------------------------------------------------------
    # 4. Risk Score (volatility + max drawdown) (0–10)
    # -----------------------------------------------------------
    def risk_score(self):
        # Portfolio volatility
        returns = np.diff(self.values) / self.values[:-1]
        vol = np.std(returns)

        # Scale volatility score (lower vol = higher score)
        vol_score = max(0, min(1 / (1 + 10 * vol), 1)) * 5  # 0–5 pts

        # Max Drawdown
        peak = np.maximum.accumulate(self.values)
        drawdowns = (self.values - peak) / peak
        max_dd = abs(drawdowns.min())

        # Scale drawdown score (smaller drawdown = higher score)
        dd_score = max(0, min(1 - max_dd, 1)) * 5  # 0–5 pts

        return round(vol_score + dd_score, 2)  # 0–10

    # -----------------------------------------------------------
    # 5. Final Portfolio Score (0–100)
    # -----------------------------------------------------------
    def total_score(self):
        stock_component = self.weighted_stock_score()      # 0–50
        sharpe_component = self.portfolio_sharpe()         # 0–25
        diversification_component = self.diversification_score()  # 0–15
        risk_component = self.risk_score()                 # 0–10

        total = stock_component + sharpe_component + diversification_component + risk_component

        return {
            "portfolio_score": round(total, 2),
            "stock_component": stock_component,
            "sharpe_component": sharpe_component,
            "diversification_component": diversification_component,
            "risk_component": risk_component
        }

