import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '../views/LandingPage.vue'
import MyStocks from '../views/my_stocks.vue'
import Profile from '../views/profile.vue'
import PortfolioAnalysis from '../views/portfolio_analysis.vue'

const routes = [
  { path: '/', name: 'LandingPage', component: LandingPage },
  { path: '/my-stocks', name: 'MyStocks', component: MyStocks },
  { path: '/profile', name: 'Profile', component: Profile },
  { path: '/portfolio-analysis', name: 'PortfolioAnalysis', component: PortfolioAnalysis }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
