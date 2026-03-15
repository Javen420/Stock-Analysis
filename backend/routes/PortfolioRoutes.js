import { Router } from "express";
import Portfolio from "../models/portfolio.js";

const router = Router();

// GET /api/portfolios — all portfolios for the authenticated user
router.get("/", async (req, res) => {
  try {
    const portfolios = await Portfolio.find({ userId: req.user.id });
    res.json(portfolios);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Server error" });
  }
});

// POST /api/portfolios — create a new portfolio
router.post("/", async (req, res) => {
  try {
    const { name, description } = req.body;
    if (!name) return res.status(400).json({ error: "Missing portfolio name" });
    if (name.length > 100)
      return res.status(400).json({ error: "Portfolio name too long (max 100 characters)" });
    if (description && description.length > 500)
      return res.status(400).json({ error: "Description too long (max 500 characters)" });

    const portfolio = await Portfolio.create({
      userId: req.user.id,
      name,
      description,
    });
    res.status(201).json(portfolio);
  } catch (err) {
    if (err.code === 11000)
      return res.status(409).json({ error: "Portfolio name already exists" });
    console.error(err);
    res.status(500).json({ error: "Server error" });
  }
});

// PUT /api/portfolios/:id/holdings — add or remove a stock from holdings
router.put("/:id/holdings", async (req, res) => {
  try {
    const { stockId, symbol, shares, averageCost, action } = req.body;
    if (!stockId && !symbol)
      return res.status(400).json({ error: "Missing stockId or symbol" });
    if (symbol && !/^[A-Za-z]{1,5}$/.test(symbol))
      return res.status(400).json({ error: "Invalid ticker symbol" });
    if (shares != null && (typeof shares !== "number" || shares <= 0 || shares > 1000000))
      return res.status(400).json({ error: "Shares must be between 0 and 1,000,000" });
    if (averageCost != null && (typeof averageCost !== "number" || averageCost <= 0 || averageCost > 1000000))
      return res.status(400).json({ error: "Average cost must be between 0 and 1,000,000" });

    const portfolio = await Portfolio.findOne({
      _id: req.params.id,
      userId: req.user.id,
    });
    if (!portfolio)
      return res.status(404).json({ error: "Portfolio not found" });

    // Match by symbol first, then stockId
    const matchHolding = (h) =>
      (symbol && h.symbol === symbol.toUpperCase()) ||
      (stockId && h.stockId && h.stockId.toString() === stockId);

    if (action === "remove") {
      portfolio.holdings = portfolio.holdings.filter((h) => !matchHolding(h));
    } else {
      const existing = portfolio.holdings.find(matchHolding);
      if (existing) {
        if (shares != null) existing.shares = shares;
        if (averageCost != null) existing.averageCost = averageCost;
      } else {
        if (shares == null || averageCost == null)
          return res
            .status(400)
            .json({ error: "Missing shares or averageCost" });
        const holding = { shares, averageCost };
        if (symbol) holding.symbol = symbol.toUpperCase();
        if (stockId) holding.stockId = stockId;
        portfolio.holdings.push(holding);
      }
    }

    await portfolio.save();
    res.json(portfolio);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Server error" });
  }
});

// DELETE /api/portfolios/:id — delete a portfolio
router.delete("/:id", async (req, res) => {
  try {
    const result = await Portfolio.findOneAndDelete({
      _id: req.params.id,
      userId: req.user.id,
    });
    if (!result) return res.status(404).json({ error: "Portfolio not found" });
    res.json({ message: "Portfolio deleted" });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Server error" });
  }
});

export default router;
