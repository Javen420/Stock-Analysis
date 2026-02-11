import { Router } from "express";
import User from "../models/user.js";

const router = Router();

// GET /api/users/:id/watchlist
router.get("/:id/watchlist", async (req, res) => {
  try {
    const user = await User.findById(req.params.id).select("watchlist");
    if (!user) return res.status(404).json({ error: "User not found" });
    res.json(user.watchlist);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Server error" });
  }
});

// PUT /api/users/:id/watchlist
router.put("/:id/watchlist", async (req, res) => {
  try {
    const { ticker, action } = req.body;
    if (!ticker) return res.status(400).json({ error: "Missing ticker" });

    const user = await User.findById(req.params.id);
    if (!user) return res.status(404).json({ error: "User not found" });

    if (action === "remove") {
      user.watchlist = user.watchlist.filter((t) => t !== ticker.toUpperCase());
    } else {
      const upper = ticker.toUpperCase();
      if (!user.watchlist.includes(upper)) user.watchlist.push(upper);
    }

    await user.save();
    res.json(user.watchlist);
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: "Server error" });
  }
});

export default router;
