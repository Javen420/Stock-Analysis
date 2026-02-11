import { Router } from "express";
import Stock from "../models/IndividualStock.js";

const router = Router();

// GET /api/stocks/:symbol — look up a stock by ticker symbol
router.get("/:symbol", async (req, res) => {
  try {
    const stock = await Stock.findOne({
      symbol: req.params.symbol.toUpperCase(),
    });
    if (!stock) return res.status(404).json({ error: "Stock not found" });
    res.json(stock);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Server error" });
  }
});

export default router;
