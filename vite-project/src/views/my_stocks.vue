<template>
  <div class="max-w-5xl mx-auto px-4 py-8">
    <!-- Not logged in -->
    <div v-if="!loggedIn" class="text-center py-20">
      <h2 class="text-2xl font-bold text-slate-700 mb-2">My Stocks</h2>
      <p class="text-slate-500">Please log in to view your portfolios and watchlist.</p>
    </div>

    <template v-else>
      <!-- Success/Error Banner -->
      <div v-if="actionMsg" class="mb-4 px-4 py-2 rounded-lg text-sm" :class="actionError ? 'bg-red-50 text-red-600' : 'bg-green-50 text-green-600'">
        {{ actionMsg }}
      </div>

      <!-- Portfolio Section -->
      <section class="mb-10">
        <div class="flex items-center justify-between mb-4">
          <h1 class="text-2xl font-bold text-slate-800">Portfolios</h1>
          <button
            @click="showCreateModal = true"
            class="bg-blue-700 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
          >
            + New Portfolio
          </button>
        </div>

        <div v-if="loadingPortfolios" class="text-slate-400 text-sm">Loading portfolios...</div>

        <div v-else-if="portfolioError" class="px-4 py-3 bg-red-50 text-red-600 rounded-lg text-sm">{{ portfolioError }}</div>

        <div v-else-if="portfolios.length" class="space-y-4">
          <div
            v-for="portfolio in portfolios"
            :key="portfolio._id"
            class="bg-white rounded-xl shadow border border-slate-200 p-5"
          >
            <div class="flex items-start justify-between mb-3">
              <div>
                <h3 class="text-lg font-semibold text-blue-700">{{ portfolio.name }}</h3>
                <p class="text-sm text-slate-500">{{ portfolio.description || 'No description' }}</p>
              </div>
              <button
                @click="confirmDelete(portfolio)"
                class="text-sm text-red-500 hover:text-red-700 transition-colors"
              >
                Delete
              </button>
            </div>

            <!-- Holdings Table -->
            <div v-if="portfolio.holdings?.length" class="overflow-x-auto">
              <table class="w-full text-sm">
                <thead>
                  <tr class="border-b border-slate-200 text-left text-slate-500">
                    <th class="py-2 pr-4">Symbol</th>
                    <th class="py-2 pr-4 text-right">Shares</th>
                    <th class="py-2 pr-4 text-right">Avg Cost</th>
                    <th class="py-2 pr-4 text-right">Price</th>
                    <th class="py-2 pr-4 text-right">Cost Basis</th>
                    <th class="py-2 pr-4 text-right">Value</th>
                    <th class="py-2 pr-4 text-right">P&L</th>
                    <th class="py-2 text-right">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr
                    v-for="holding in portfolio.holdings"
                    :key="holding.symbol || holding.stockId"
                    class="border-b border-slate-100"
                  >
                    <td class="py-2 pr-4 font-medium text-blue-700">
                      <router-link :to="`/stock/${holding.symbol || holding.stockId}`" class="hover:underline">
                        {{ holding.symbol || holding.stockId }}
                      </router-link>
                    </td>
                    <td class="py-2 pr-4 text-right text-slate-600">{{ holding.shares }}</td>
                    <td class="py-2 pr-4 text-right text-slate-600">${{ holding.averageCost?.toFixed(2) }}</td>
                    <td class="py-2 pr-4 text-right text-slate-600">
                      {{ prices[holding.symbol || holding.stockId] != null ? '$' + prices[holding.symbol || holding.stockId].toFixed(2) : '...' }}
                    </td>
                    <td class="py-2 pr-4 text-right text-slate-600">${{ formatMoney(holdingCost(holding)) }}</td>
                    <td class="py-2 pr-4 text-right font-medium text-slate-800">${{ formatMoney(holdingValue(holding)) }}</td>
                    <td class="py-2 pr-4 text-right" :class="holdingValue(holding) != null && holdingValue(holding) - holdingCost(holding) >= 0 ? 'text-green-600' : 'text-red-600'">
                      <template v-if="holdingValue(holding) != null">
                        {{ holdingValue(holding) - holdingCost(holding) >= 0 ? '+' : '' }}${{ formatMoney(holdingValue(holding) - holdingCost(holding)) }}
                      </template>
                      <template v-else>...</template>
                    </td>
                    <td class="py-2 text-right space-x-2">
                      <button
                        @click="openEditHolding(portfolio, holding)"
                        class="text-blue-600 hover:text-blue-800 text-xs"
                      >
                        Edit
                      </button>
                      <button
                        @click="removeHolding(portfolio._id, holding.symbol || holding.stockId)"
                        class="text-red-500 hover:text-red-700 text-xs"
                      >
                        Remove
                      </button>
                    </td>
                  </tr>
                </tbody>
                <tfoot>
                  <tr class="border-t-2 border-slate-300 font-semibold text-slate-800">
                    <td class="py-2 pr-4" colspan="4">Total</td>
                    <td class="py-2 pr-4 text-right">${{ formatMoney(portfolioTotalCost(portfolio)) }}</td>
                    <td class="py-2 pr-4 text-right">${{ formatMoney(portfolioTotalValue(portfolio)) }}</td>
                    <td class="py-2 pr-4 text-right" :class="portfolioTotalValue(portfolio) != null && portfolioTotalValue(portfolio) - portfolioTotalCost(portfolio) >= 0 ? 'text-green-600' : 'text-red-600'">
                      <template v-if="portfolioTotalValue(portfolio) != null">
                        {{ portfolioTotalValue(portfolio) - portfolioTotalCost(portfolio) >= 0 ? '+' : '' }}${{ formatMoney(portfolioTotalValue(portfolio) - portfolioTotalCost(portfolio)) }}
                      </template>
                      <template v-else>...</template>
                    </td>
                    <td></td>
                  </tr>
                </tfoot>
              </table>
            </div>

            <p v-else class="text-sm text-slate-400 mt-1">
              No holdings yet. Search for stocks to add them.
            </p>
          </div>
        </div>

        <div v-else class="bg-white rounded-xl border border-dashed border-slate-300 p-8 text-center">
          <p class="text-slate-400 mb-3">No portfolios yet. Create one to start tracking your investments.</p>
          <button
            @click="showCreateModal = true"
            class="bg-blue-700 hover:bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
          >
            + Create Portfolio
          </button>
        </div>
      </section>

      <!-- Watchlist Section -->
      <section>
        <h1 class="text-2xl font-bold text-slate-800 mb-4">Watchlist</h1>

        <div v-if="loadingWatchlist" class="text-slate-400 text-sm">Loading watchlist...</div>

        <div v-else-if="watchlistError" class="px-4 py-3 bg-red-50 text-red-600 rounded-lg text-sm">{{ watchlistError }}</div>

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

    <!-- Create Portfolio Modal -->
    <div
      v-if="showCreateModal"
      class="fixed inset-0 bg-black/40 flex items-center justify-center z-50"
      @click.self="showCreateModal = false"
    >
      <div class="bg-white rounded-xl shadow-xl w-full max-w-md mx-4 p-6">
        <h3 class="text-lg font-semibold text-slate-800 mb-4">Create Portfolio</h3>

        <label class="block text-sm font-medium text-slate-600 mb-1">Name</label>
        <input
          v-model="newPortfolioName"
          type="text"
          maxlength="100"
          placeholder="e.g. Tech Growth"
          class="w-full border border-slate-300 rounded-lg px-3 py-2 mb-4 text-slate-800"
        />

        <label class="block text-sm font-medium text-slate-600 mb-1">Description (optional)</label>
        <input
          v-model="newPortfolioDesc"
          type="text"
          maxlength="500"
          placeholder="e.g. Long-term tech holdings"
          class="w-full border border-slate-300 rounded-lg px-3 py-2 mb-4 text-slate-800"
        />

        <div class="flex justify-end gap-3">
          <button
            @click="showCreateModal = false"
            class="px-4 py-2 text-sm text-slate-600 hover:text-slate-800 transition-colors"
          >
            Cancel
          </button>
          <button
            @click="createPortfolio"
            :disabled="!newPortfolioName.trim() || creatingPortfolio"
            class="bg-blue-700 hover:bg-blue-600 disabled:opacity-50 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
          >
            {{ creatingPortfolio ? 'Creating...' : 'Create' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div
      v-if="showDeleteModal"
      class="fixed inset-0 bg-black/40 flex items-center justify-center z-50"
      @click.self="showDeleteModal = false"
    >
      <div class="bg-white rounded-xl shadow-xl w-full max-w-sm mx-4 p-6">
        <h3 class="text-lg font-semibold text-slate-800 mb-2">Delete Portfolio</h3>
        <p class="text-sm text-slate-600 mb-4">
          Are you sure you want to delete <strong>{{ deleteTarget?.name }}</strong>? This cannot be undone.
        </p>
        <div class="flex justify-end gap-3">
          <button
            @click="showDeleteModal = false"
            class="px-4 py-2 text-sm text-slate-600 hover:text-slate-800 transition-colors"
          >
            Cancel
          </button>
          <button
            @click="deletePortfolio"
            :disabled="deletingPortfolio"
            class="bg-red-600 hover:bg-red-500 disabled:opacity-50 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
          >
            {{ deletingPortfolio ? 'Deleting...' : 'Delete' }}
          </button>
        </div>
      </div>
    </div>

    <!-- Edit Holding Modal -->
    <div
      v-if="showEditModal"
      class="fixed inset-0 bg-black/40 flex items-center justify-center z-50"
      @click.self="showEditModal = false"
    >
      <div class="bg-white rounded-xl shadow-xl w-full max-w-sm mx-4 p-6">
        <h3 class="text-lg font-semibold text-slate-800 mb-4">
          Edit {{ editHolding?.symbol }} in {{ editPortfolio?.name }}
        </h3>

        <label class="block text-sm font-medium text-slate-600 mb-1">Shares</label>
        <input
          v-model.number="editShares"
          type="number"
          min="0"
          step="any"
          class="w-full border border-slate-300 rounded-lg px-3 py-2 mb-4 text-slate-800"
        />

        <label class="block text-sm font-medium text-slate-600 mb-1">Average Cost ($)</label>
        <input
          v-model.number="editAvgCost"
          type="number"
          min="0"
          step="any"
          class="w-full border border-slate-300 rounded-lg px-3 py-2 mb-4 text-slate-800"
        />

        <div class="flex justify-end gap-3">
          <button
            @click="showEditModal = false"
            class="px-4 py-2 text-sm text-slate-600 hover:text-slate-800 transition-colors"
          >
            Cancel
          </button>
          <button
            @click="updateHolding"
            :disabled="!editShares || !editAvgCost || updatingHolding"
            class="bg-blue-700 hover:bg-blue-600 disabled:opacity-50 text-white px-4 py-2 rounded-lg text-sm font-medium transition-colors"
          >
            {{ updatingHolding ? 'Saving...' : 'Save' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import StockCard from '../components/StockCard.vue'

const loggedIn = ref(false)
const portfolios = ref([])
const watchlist = ref([])
const loadingPortfolios = ref(true)
const loadingWatchlist = ref(true)
const portfolioError = ref('')
const watchlistError = ref('')
const actionMsg = ref('')
const actionError = ref(false)
const prices = ref({}) // { AAPL: 182.50, MSFT: 415.20, ... }

// Create portfolio state
const showCreateModal = ref(false)
const newPortfolioName = ref('')
const newPortfolioDesc = ref('')
const creatingPortfolio = ref(false)

// Delete portfolio state
const showDeleteModal = ref(false)
const deleteTarget = ref(null)
const deletingPortfolio = ref(false)

// Edit holding state
const showEditModal = ref(false)
const editPortfolio = ref(null)
const editHolding = ref(null)
const editShares = ref(null)
const editAvgCost = ref(null)
const updatingHolding = ref(false)

function getHeaders() {
  return {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${localStorage.getItem('token')}`
  }
}

function showAction(msg, isError = false) {
  actionMsg.value = msg
  actionError.value = isError
  setTimeout(() => { actionMsg.value = '' }, 3000)
}

function holdingValue(holding) {
  const symbol = holding.symbol || holding.stockId
  const price = prices.value[symbol]
  if (price == null) return null
  return holding.shares * price
}

function holdingCost(holding) {
  return holding.shares * (holding.averageCost || 0)
}

function portfolioTotalValue(portfolio) {
  if (!portfolio.holdings?.length) return null
  let total = 0
  for (const h of portfolio.holdings) {
    const val = holdingValue(h)
    if (val == null) return null
    total += val
  }
  return total
}

function portfolioTotalCost(portfolio) {
  if (!portfolio.holdings?.length) return 0
  return portfolio.holdings.reduce((sum, h) => sum + holdingCost(h), 0)
}

function formatMoney(n) {
  if (n == null) return '...'
  return n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

async function fetchPrices() {
  const symbols = new Set()
  for (const p of portfolios.value) {
    for (const h of (p.holdings || [])) {
      symbols.add(h.symbol || h.stockId)
    }
  }
  const fetches = [...symbols].map(async (symbol) => {
    try {
      const res = await fetch(`http://localhost:8002/stocks/${symbol}`)
      if (res.ok) {
        const data = await res.json()
        if (data.prices?.length) {
          prices.value[symbol] = Number(data.prices[0].price)
        }
      }
    } catch { /* skip */ }
  })
  await Promise.all(fetches)
}

async function fetchPortfolios() {
  try {
    const res = await fetch('http://localhost:5000/api/portfolios', { headers: getHeaders() })
    if (res.ok) {
      portfolios.value = await res.json()
    }
  } catch (err) {
    console.error('Failed to fetch portfolios:', err)
  }
}

// Create portfolio
async function createPortfolio() {
  creatingPortfolio.value = true
  try {
    const res = await fetch('http://localhost:5000/api/portfolios', {
      method: 'POST',
      headers: getHeaders(),
      body: JSON.stringify({
        name: newPortfolioName.value.trim(),
        description: newPortfolioDesc.value.trim()
      })
    })
    const data = await res.json()
    if (!res.ok) {
      showAction(data.error || 'Failed to create portfolio', true)
      return
    }
    portfolios.value.push(data)
    showCreateModal.value = false
    newPortfolioName.value = ''
    newPortfolioDesc.value = ''
    showAction('Portfolio created!')
  } catch {
    showAction('Network error', true)
  } finally {
    creatingPortfolio.value = false
  }
}

// Delete portfolio
function confirmDelete(portfolio) {
  deleteTarget.value = portfolio
  showDeleteModal.value = true
}

async function deletePortfolio() {
  deletingPortfolio.value = true
  try {
    const res = await fetch(`http://localhost:5000/api/portfolios/${deleteTarget.value._id}`, {
      method: 'DELETE',
      headers: getHeaders()
    })
    if (!res.ok) {
      showAction('Failed to delete portfolio', true)
      return
    }
    portfolios.value = portfolios.value.filter(p => p._id !== deleteTarget.value._id)
    showDeleteModal.value = false
    showAction('Portfolio deleted')
  } catch {
    showAction('Network error', true)
  } finally {
    deletingPortfolio.value = false
  }
}

// Edit holding
function openEditHolding(portfolio, holding) {
  editPortfolio.value = portfolio
  editHolding.value = { symbol: holding.symbol || holding.stockId }
  editShares.value = holding.shares
  editAvgCost.value = holding.averageCost
  showEditModal.value = true
}

async function updateHolding() {
  updatingHolding.value = true
  try {
    const res = await fetch(`http://localhost:5000/api/portfolios/${editPortfolio.value._id}/holdings`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify({
        symbol: editHolding.value.symbol,
        shares: editShares.value,
        averageCost: editAvgCost.value
      })
    })
    if (!res.ok) {
      showAction('Failed to update holding', true)
      return
    }
    const updated = await res.json()
    const idx = portfolios.value.findIndex(p => p._id === editPortfolio.value._id)
    if (idx !== -1) portfolios.value[idx] = updated
    showEditModal.value = false
    showAction('Holding updated!')
  } catch {
    showAction('Network error', true)
  } finally {
    updatingHolding.value = false
  }
}

// Remove holding
async function removeHolding(portfolioId, symbol) {
  try {
    const res = await fetch(`http://localhost:5000/api/portfolios/${portfolioId}/holdings`, {
      method: 'PUT',
      headers: getHeaders(),
      body: JSON.stringify({ symbol, action: 'remove' })
    })
    if (!res.ok) {
      showAction('Failed to remove holding', true)
      return
    }
    const updated = await res.json()
    const idx = portfolios.value.findIndex(p => p._id === portfolioId)
    if (idx !== -1) portfolios.value[idx] = updated
    showAction('Holding removed')
  } catch {
    showAction('Network error', true)
  }
}

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) {
    loadingPortfolios.value = false
    loadingWatchlist.value = false
    return
  }
  loggedIn.value = true

  // Fetch portfolios
  try {
    const res = await fetch('http://localhost:5000/api/portfolios', { headers: getHeaders() })
    if (res.ok) {
      portfolios.value = await res.json()
    } else {
      portfolioError.value = 'Failed to load portfolios.'
    }
  } catch (err) {
    portfolioError.value = 'Could not connect to server.'
    console.error('Failed to fetch portfolios:', err)
  } finally {
    loadingPortfolios.value = false
  }

  // Fetch current prices for all holdings
  if (portfolios.value.length) {
    fetchPrices()
  }

  // Fetch watchlist
  try {
    const user = JSON.parse(localStorage.getItem('user') || '{}')
    const res = await fetch(`http://localhost:5000/api/users/${user.id}/watchlist`, { headers: getHeaders() })
    if (res.ok) {
      const data = await res.json()
      watchlist.value = data.watchlist || []
    } else {
      watchlistError.value = 'Failed to load watchlist.'
    }
  } catch (err) {
    watchlistError.value = 'Could not connect to server.'
    console.error('Failed to fetch watchlist:', err)
  } finally {
    loadingWatchlist.value = false
  }
})
</script>
