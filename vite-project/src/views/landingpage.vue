<template>
  <div class="max-w-5xl mx-auto px-4 py-8">
    <!-- Hero Section -->
    <section class="text-center py-12">
      <h1 class="text-4xl font-bold text-blue-800 mb-4">Stock Finder</h1>
      <p class="text-lg text-slate-600 mb-8">
        Search, analyze, and grade stocks. Build portfolios and track your investments.
      </p>

      <!-- Search Bar -->
      <Search @select="goToStock" />
    </section>

    <!-- Quick Stats (logged-in users) -->
    <section v-if="loggedIn && portfolios.length" class="mb-10">
      <h2 class="text-xl font-semibold text-slate-700 mb-4">Your Portfolios</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="portfolio in portfolios"
          :key="portfolio._id"
          class="bg-white rounded-xl shadow p-4 border border-slate-200"
        >
          <h3 class="font-semibold text-blue-700">{{ portfolio.name }}</h3>
          <p class="text-sm text-slate-500">{{ portfolio.description || 'No description' }}</p>
          <p class="text-sm text-slate-400 mt-2">
            {{ portfolio.holdings?.length || 0 }} holdings
          </p>
        </div>
      </div>
    </section>

    <!-- Featured / Example Stocks -->
    <section>
      <h2 class="text-xl font-semibold text-slate-700 mb-4">Popular Stocks</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <StockCard
          v-for="symbol in featuredSymbols"
          :key="symbol"
          :symbol="symbol"
        />
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Search from '../components/search.vue'
import StockCard from '../components/StockCard.vue'

const loggedIn = ref(false)
const portfolios = ref([])
const featuredSymbols = ref(['AAPL', 'MSFT', 'GOOGL'])

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (token) {
    loggedIn.value = true
    try {
      const res = await fetch('http://localhost:5000/api/portfolios', {
        headers: { Authorization: `Bearer ${token}` }
      })
      if (res.ok) {
        portfolios.value = await res.json()
      }
    } catch {
      // backend not running or endpoint not ready yet
    }
  }
})

function goToStock(symbol) {
  // For now just scroll or could navigate to a stock detail page later
  console.log('Selected stock:', symbol)
}
</script>
