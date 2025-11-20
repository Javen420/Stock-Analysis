import mongoose from 'mongoose';

const userSchema = new mongoose.Schema({
  username: String,
  email: String,
  password: String,
  savedStocks: [
    { symbol: String, name: String, price: Number, addedAt: { type: Date, default: Date.now } }
  ]
});

const User = mongoose.model('User', userSchema);
export default User;
