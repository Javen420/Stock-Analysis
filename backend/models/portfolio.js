import mongoose from 'mongoose';

const portfolioSchema = new mongoose.Schema({
  user: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  stocks: [
    {
      symbol: String,
      name: String,
      shares: Number,
      boughtAt: { type: Date, default: Date.now }
    }
  ]
});

const Portfolio = mongoose.model('Portfolio', portfolioSchema);
export default Portfolio;
