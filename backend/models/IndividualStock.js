//for searching up individual stock, need to show historical price and get the other information 
// regarding stock, might have to use api, like seeking alpha

import mongoose from "mongoose";

const DailyPriceSchema = new mongoose.Schema({
  date: { type: Date, required: true },
  open: Number,
  high: Number,
  low: Number,
  close: Number,
  volume: Number
}, { _id: false });

const StockSchema = new mongoose.Schema({
  // Core info
  symbol: { type: String, required: true, unique: true },
  companyName: String,
  exchange: String,
  sector: String,
  industry: String,
  description: String,
  logoUrl: String,

  // Fundamentals (update monthly/quarterly)
  marketCap: Number,
  peRatio: Number,
  psRatio: Number,
  pbRatio: Number,
  freeCashFlow: Number,
  revenue: Number,
  ebitda: Number,
  dividendYield: Number,

  // Cached short-term price
  cachedPrice: Number,
  priceLastUpdated: Date,

  // Optional: store daily historic candles
  history: [DailyPriceSchema],

  lastFundamentalUpdate: Date
});

export default mongoose.model("Stock", StockSchema);

