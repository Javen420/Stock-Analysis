<template>
  <div class="max-w-5xl mx-auto px-4 py-8">
    <!-- Loading -->
    <div v-if="loading" class="text-center py-20">
      <p class="text-slate-400">Loading stock data...</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="text-center py-20">
      <p class="text-red-500">{{ error }}</p>
      <router-link to="/" class="text-blue-600 hover:underline text-sm mt-2 inline-block">Back to Home</router-link>
    </div>

    <template v-else-if="stock">
      <!-- Header -->
      <section class="mb-6">
        <router-link to="/" class="text-sm text-blue-600 hover:underline mb-3 inline-block">&larr; Back</router-link>
        <div class="flex items-start justify-between flex-wrap gap-4">
          <div>
            <h1 class="text-3xl font-bold text-slate-800">{{ stock.symbol }}</h1>
            <p class="text-lg text-slate-600">{{ stock.name }}</p>
            <div class="flex gap-3 mt-1 text-sm text-slate-400">
              <span v-if="stock.exchange">{{ stock.exchange }}</span>
              <span v-if="stock.sector">{{ stock.sector }}</span>
              <span v-if="stock.industry">{{ stock.industry }}</span>
            </div>
          </div>
          <div v-if="latestPrice" class="text-right">
            <p class="text-3xl font-bold text-slate-800">${{ latestPrice }}</p>
            <p v-if="priceChange !== null" class="text-sm font-medium" :class="priceChange >= 0 ? 'text-green-600' : 'text-red-600'">
              {{ priceChange >= 0 ? '+' : '' }}{{ priceChange.toFixed(2) }}
              ({{ priceChangePercent >= 0 ? '+' : '' }}{{ priceChangePercent.toFixed(2) }}%)
            </p>
          </div>
        </div>
      </section>

      <!-- Action Buttons -->
      <section class="flex gap-3 mb-6">
        <button
          v-if="loggedIn"
          @click="toggleWatchlist"
          :disabled="watchlistLoading"
          class="px-4 py-2 rounded-lg text-sm font-medium transition-colors"
          :class="isInWatchlist
            ? 'bg-yellow-100 text-yellow-700 hover:bg-yellow-200'
            : 'bg-slate-100 text-slate-700 hover:bg-slate-200'"
        >
          {{ isInWatchlist ? 'In Watchlist' : 'Add to Watchlist' }}
        </button>
        <button
          v-if="loggedIn"
          @click="showPortfolioModal = true"
          class="bg-blue-700 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
        >
          Add to Portfolio
        </button>
        <p v-if="!loggedIn" class="text-sm text-slate-400">Log in to add to watchlist or portfolio.</p>
      </section>

      <!-- Success/Error messages -->
      <div v-if="actionMsg" class="mb-4 px-4 py-2 rounded-lg text-sm" :class="actionError ? 'bg-red-50 text-red-600' : 'bg-green-50 text-green-600'">
        {{ actionMsg }}
      </div>

      <!-- Price Chart -->
      <section class="mb-8">
        <h2 class="text-xl font-semibold text-slate-700 mb-3">Price History</h2>
        <div class="bg-white rounded-xl shadow border border-slate-200 p-4">
          <Charts
            v-if="stock.prices && stock.prices.length"
            :prices="stock.prices"
            :height="250"
          />
          <p v-else class="text-slate-400 text-sm text-center py-8">No price data available.</p>
        </div>
      </section>

      <!-- Recent Prices Table -->
      <section v-if="stock.prices && stock.prices.length" class="mb-8">
        <h2 class="text-xl font-semibold text-slate-700 mb-3">Recent Prices</h2>
        <div class="bg-white rounded-xl shadow border border-slate-200 overflow-x-auto">
          <table class="w-full text-sm">
            <thead>
              <tr class="border-b border-slate-200 text-left text-slate-500">
                <th class="px-4 py-3">Date</th>
                <th class="px-4 py-3 text-right">Close</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(p, i) in stock.prices.slice(0, 20)"
                :key="i"
                class="border-b border-slate-100 hover:bg-slate-50"
              >
                <td class="px-4 py-2 text-slate-600">{{ p.date }}</td>
                <td class="px-4 py-2 text-right font-medium text-slate-800">${{ Number(p.price).toFixed(2) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Company Description -->
      <section v-if="stock.description" class="mb-8">
        <h2 class="text-xl font-semibold text-slate-700 mb-3">About</h2>
        <div class="bg-white rounded-xl shadow border border-slate-200 p-5">
          <p class="text-sm text-slate-600 leading-relaxed">{{ stock.description }}</p>
        </div>
      </section>
    </template>

    <!-- Add to Portfolio Modal -->
    <div
      v-if="showPortfolioModal"
      class="fixed inset-0 bg-black/40 flex items-center justify-center z-50"
      @click.self="showPortfolioModal = false"
    >
      <div class="bg-white rounded-xl shadow-xl w-full max-w-md mx-4 p-6">
        <h3 class="text-lg font-semibold text-slate-800 mb-4">Add {{ stock?.symbol }} to Portfolio</h3>

        <div v-if="!portfolios.length" class="text-sm text-slate-400 mb-4">
          No portfolios found. Create one in My Stocks first.
        </div>

        <template v-else>
          <!-- Portfolio Select -->
          <label class="block text-sm font-medium text-slate-600 mb-1">Portfolio</label>
          <select v-model="selectedPortfolioId" class="w-full border border-slate-300 rounded-lg px-3 py-2 mb-4 text-slate-800">
            <option value="" disabled>Select a portfolio</option>
            <option v-for="p in portfolios" :key="p._id" :value="p._id">{{ p.name }}</option>
          </select>

          <!-- Shares -->
          <label class="block text-sm font-medium text-slate-600 mb-1">Shares</label>
          <input
            v-model.number="modalShares"
            type="number"
            min="0"
            step="any"
            placeholder="e.g. 10"
            class="w-full border border-slate-300 rounded-lg px-3 py-2 mb-4 text-slate-800"
          />

          <!-- Average Cost -->
          <label class="block text-sm font-medium text-slate-600 mb-1">Average Cost ($)</label>
          <input
            v-model.number="modalAvgCost"
            type="number"
            min="0"
            step="any"
            :placeholder="latestPrice ? `e.g. ${latestPrice}` : 'e.g. 150.00'"
            class="w-full border border-slate-300 rounded-lg px-3 py-2 mb-4 text-slate-800"
          />
        </template>

        <div class="flex justify-end gap-3">
          <button
            @click="showPortfolioModal = false"
            class="px-4 py-2 text-sm text-slate-600 hover:text-slate-800 transition-colors"
          >
            Cancel
          </button>
          <button
            v-if="portfolios.length"
            @click="addToPortfolio"
            :disabled="!selectedPortfolioId || !modalShares || !modalAvgCost || addingToPortfolio"
            class="bg-blue-700 hover:bg-blue-600 disabled:opacity-50 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
          >
            {{ addingToPortfolio ? 'Adding...' : 'Add' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import Charts from '../components/Charts.vue'

const route = useRoute()
const symbolParam = route.params.symbol.toUpperCase()

const stock = ref(null)
const loading = ref(true)
const error = ref(null)
const loggedIn = ref(false)
const watchlist = ref([])
const portfolios = ref([])
const watchlistLoading = ref(false)
const actionMsg = ref('')
const actionError = ref(false)

// Portfolio modal state
const showPortfolioModal = ref(false)
const selectedPortfolioId = ref('')
const modalShares = ref(null)
const modalAvgCost = ref(null)
const addingToPortfolio = ref(false)

const latestPrice = computed(() => {
  if (!stock.value?.prices?.length) return null
  return Number(stock.value.prices[0].price).toFixed(2)
})

const priceChange = computed(() => {
  if (!stock.value?.prices?.length || stock.value.prices.length < 2) return null
  return Number(stock.value.prices[0].price) - Number(stock.value.prices[1].price)
})

const priceChangePercent = computed(() => {
  if (priceChange.value === null) return null
  const prev = Number(stock.value.prices[1].price)
  return prev ? (priceChange.value / prev) * 100 : 0
})

const isInWatchlist = computed(() => watchlist.value.includes(symbolParam))

function showAction(msg, isError = false) {
  actionMsg.value = msg
  actionError.value = isError
  setTimeout(() => { actionMsg.value = '' }, 3000)
}

onMounted(async () => {
  const token = localStorage.getItem('token')
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  if (token && user.id) {
    loggedIn.value = true
  }

  // Fetch stock data
  try {
    const res = await fetch(`http://localhost:8000/stocks/${symbolParam}`)
    if (!res.ok) {
      const data = await res.json().catch(() => ({}))
      error.value = data.detail || `Ticker "${symbolParam}" not found`
      return
    }
    stock.value = await res.json()
  } catch {
    error.value = 'Could not connect to stock API.'
  } finally {
    loading.value = false
  }

  // Fetch user data if logged in
  if (loggedIn.value) {
    const headers = { Authorization: `Bearer ${token}` }
    // Fetch watchlist and portfolios in parallel
    try {
      const [wlRes, pfRes] = await Promise.all([
        fetch(`http://localhost:5000/api/users/${user.id}/watchlist`, { headers }),
        fetch('http://localhost:5000/api/portfolios', { headers })
      ])
      if (wlRes.ok) {
        const data = await wlRes.json()
        watchlist.value = data.watchlist || []
      }
      if (pfRes.ok) {
        portfolios.value = await pfRes.json()
      }
    } catch (err) {
      console.error('Failed to fetch user data:', err)
    }
  }
})

async function toggleWatchlist() {
  const token = localStorage.getItem('token')
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  if (!token || !user.id) return

  watchlistLoading.value = true
  const action = isInWatchlist.value ? 'remove' : 'add'

  try {
    const res = await fetch(`http://localhost:5000/api/users/${user.id}/watchlist`, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ ticker: symbolParam, action })
    })
    if (res.ok) {
      const data = await res.json()
      watchlist.value = data.watchlist || []
      showAction(action === 'add' ? `${symbolParam} added to watchlist` : `${symbolParam} removed from watchlist`)
    }
  } catch {
    showAction('Failed to update watchlist', true)
  } finally {
    watchlistLoading.value = false
  }
}

async function addToPortfolio() {
  const token = localStorage.getItem('token')
  if (!token || !selectedPortfolioId.value) return

  addingToPortfolio.value = true

  try {
    const res = await fetch(`http://localhost:5000/api/portfolios/${selectedPortfolioId.value}/holdings`, {
      method: 'PUT',
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        symbol: symbolParam,
        shares: modalShares.value,
        averageCost: modalAvgCost.value
      })
    })

    if (res.ok) {
      showPortfolioModal.value = false
      modalShares.value = null
      modalAvgCost.value = null
      selectedPortfolioId.value = ''
      showAction(`${symbolParam} added to portfolio`)
    } else {
      const data = await res.json().catch(() => ({}))
      showAction(data.error || 'Failed to add to portfolio', true)
    }
  } catch {
    showAction('Failed to add to portfolio', true)
  } finally {
    addingToPortfolio.value = false
  }
}
</script>
