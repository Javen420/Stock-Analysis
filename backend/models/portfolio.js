import mongoose from "mongoose";

const PortfolioStockSchema = new mongoose.Schema({
  stockId: { 
    type: mongoose.Schema.Types.ObjectId,
    ref: "Stock",
    required: true
  },
  shares: { type: Number, required: true },
  averageCost: { type: Number, required: true }
}, { _id: false });

const PortfolioSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: "User",
    required: true
  },

  name: {
    type: String,
    required: true
  },

  description: {
    type: String,
    default: ""
  },

  // Portfolio holds references to stock documents
  holdings: {
    type: [PortfolioStockSchema],
    default: []
  },

  // Optional: used for charts and analytics
  history: [{
    date: { type: Date, default: Date.now },
    totalValue: Number
  }],

  createdAt: {
    type: Date,
    default: Date.now
  }
});

// Prevent user from making two portfolios with the same name
PortfolioSchema.index({ userId: 1, name: 1 }, { unique: true });

export default mongoose.model("Portfolio", PortfolioSchema);
