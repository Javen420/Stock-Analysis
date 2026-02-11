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
    const { stockId, shares, averageCost, action } = req.body;
    if (!stockId) return res.status(400).json({ error: "Missing stockId" });

    const portfolio = await Portfolio.findOne({
      _id: req.params.id,
      userId: req.user.id,
    });
    if (!portfolio)
      return res.status(404).json({ error: "Portfolio not found" });

    if (action === "remove") {
      portfolio.holdings = portfolio.holdings.filter(
        (h) => h.stockId.toString() !== stockId
      );
    } else {
      const existing = portfolio.holdings.find(
        (h) => h.stockId.toString() === stockId
      );
      if (existing) {
        if (shares != null) existing.shares = shares;
        if (averageCost != null) existing.averageCost = averageCost;
      } else {
        if (shares == null || averageCost == null)
          return res
            .status(400)
            .json({ error: "Missing shares or averageCost" });
        portfolio.holdings.push({ stockId, shares, averageCost });
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
