import mongoose from "mongoose";

const PriceHistorySchema = new mongoose.Schema({
  stockId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "Stock",
    required: true
  },

  date: {
    type: Date,
    required: true
  },

  open: Number,
  high: Number,
  low: Number,
  close: Number,
  volume: Number,

  // optional: adjusted close (useful for dividends/splits)
  adjClose: Number
});

// Fast lookup: find all candles for a stock sorted by date
PriceHistorySchema.index({ stockId: 1, date: 1 }, { unique: true });

export default mongoose.model("PriceHistory", PriceHistorySchema);
