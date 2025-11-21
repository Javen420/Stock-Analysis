//records the stocks that the user has saved/liked?
// dk how this will be different from the portfolio schema

import mongoose from 'mongoose';

const IndividualStockSchema = new mongoose.Schema({
  symbol: { type: string, required:true, unique: true },
  name: {type: string, required:true, unique: true },
  Current_Price: {type: Float16Array, required:true, unique: true}
});

const IndividualStock = mongoose.model('IndividualStock', IndividualStockSchema);
export default IndividualStock;
