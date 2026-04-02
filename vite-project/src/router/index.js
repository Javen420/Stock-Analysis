import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '../views/LandingPage.vue'

const routes = [
  {
    path: '/',
    name: 'Landing',
    component: LandingPage
  },
  {
    path: '/features',
    name: 'Features',
    component: () => import('../views/FeaturesPage.vue')
  },
  {
    path: '/philosophy',
    name: 'Philosophy',
    component: () => import('../views/PhilosophyPage.vue')
  },
  {
    path: '/protocol',
    name: 'Protocol',
    component: () => import('../views/ProtocolPage.vue')
  },

  // Interactive Analysis App routes
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('../views/Dashboard.vue')
  },
  {
    path: '/stock/:symbol',
    name: 'StockDetail',
    component: () => import('../views/StockDetail.vue')
  },
  {
    path: '/portfolio/new',
    name: 'CustomPortfolio',
    component: () => import('../views/CustomPortfolio.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
