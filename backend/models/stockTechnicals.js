import mongoose from "mongoose";

const AnalyticsSchema = new mongoose.Schema({
  stockId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "Stock",
    required: true,
    unique: true
  },

  fundamentals: {
    pe: Number,
    eps: Number,
    pb: Number,
    fcf: Number,
    dividendYield: Number,
    revenueGrowth: Number,
    profitMargin: Number,
    debtToEquity: Number,
    roe: Number,
    roa: Number
  },

  technicals: {
    rsi: Number,
    macd: {
      macd: Number,
      signal: Number,
      histogram: Number
    },
    sma20: Number,
    sma50: Number,
    sma200: Number,
  },

  scoring: {
    valueScore: Number,
    growthScore: Number,
    momentumScore: Number,
    overallScore: Number // example: 0–100 rating
  },

  lastUpdated: {
    type: Date,
    default: Date.now
  }
});

export default mongoose.model("Analytics", AnalyticsSchema);
