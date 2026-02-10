<template>
  <div class="max-w-5xl mx-auto px-4 py-8">
    <!-- Not logged in -->
    <div v-if="!loggedIn" class="text-center py-20">
      <h2 class="text-2xl font-bold text-slate-700 mb-2">My Stocks</h2>
      <p class="text-slate-500">Please log in to view your portfolios and watchlist.</p>
    </div>

    <template v-else>
      <!-- Portfolio Section -->
      <section class="mb-10">
        <h1 class="text-2xl font-bold text-slate-800 mb-4">Portfolios</h1>

        <div v-if="loadingPortfolios" class="text-slate-400 text-sm">Loading portfolios...</div>

        <div v-else-if="portfolios.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <div
            v-for="portfolio in portfolios"
            :key="portfolio._id"
            class="bg-white rounded-xl shadow border border-slate-200 p-4 hover:shadow-md transition-shadow"
          >
            <h3 class="text-lg font-semibold text-blue-700">{{ portfolio.name }}</h3>
            <p class="text-sm text-slate-500 mt-1">{{ portfolio.description || 'No description' }}</p>

            <div class="mt-3 space-y-1">
              <div
                v-for="holding in portfolio.holdings"
                :key="holding.stockId"
                class="flex justify-between text-sm text-slate-600"
              >
                <span>{{ holding.symbol || holding.stockId }}</span>
                <span>{{ holding.shares }} shares @ ${{ holding.averageCost?.toFixed(2) }}</span>
              </div>
            </div>

            <p v-if="!portfolio.holdings?.length" class="text-sm text-slate-400 mt-2">
              No holdings yet
            </p>
          </div>
        </div>

        <div v-else class="bg-white rounded-xl border border-dashed border-slate-300 p-8 text-center">
          <p class="text-slate-400">No portfolios yet. Create one to start tracking your investments.</p>
        </div>
      </section>

      <!-- Watchlist Section -->
      <section>
        <h1 class="text-2xl font-bold text-slate-800 mb-4">Watchlist</h1>

        <div v-if="loadingWatchlist" class="text-slate-400 text-sm">Loading watchlist...</div>

        <div v-else-if="watchlist.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          <StockCard
            v-for="symbol in watchlist"
            :key="symbol"
            :symbol="symbol"
          />
        </div>

        <div v-else class="bg-white rounded-xl border border-dashed border-slate-300 p-8 text-center">
          <p class="text-slate-400">Your watchlist is empty. Search for stocks to add them here.</p>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import StockCard from '../components/StockCard.vue'

const loggedIn = ref(false)
const portfolios = ref([])
const watchlist = ref([])
const loadingPortfolios = ref(true)
const loadingWatchlist = ref(true)

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) {
    loadingPortfolios.value = false
    loadingWatchlist.value = false
    return
  }
  loggedIn.value = true

  const headers = { Authorization: `Bearer ${token}` }

  // Fetch portfolios
  try {
    const res = await fetch('http://localhost:5000/api/portfolios', { headers })
    if (res.ok) {
      portfolios.value = await res.json()
    }
  } catch {
    // endpoint not ready yet
  } finally {
    loadingPortfolios.value = false
  }

  // Fetch watchlist (stored on user object)
  try {
    const user = JSON.parse(localStorage.getItem('user') || '{}')
    const res = await fetch(`http://localhost:5000/api/users/${user.id}/watchlist`, { headers })
    if (res.ok) {
      const data = await res.json()
      watchlist.value = data.watchlist || []
    }
  } catch {
    // endpoint not ready yet
  } finally {
    loadingWatchlist.value = false
  }
})
</script>
