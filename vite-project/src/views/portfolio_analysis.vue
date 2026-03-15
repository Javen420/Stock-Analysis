<template>
  <div class="max-w-6xl mx-auto px-4 py-8">
    <!-- Not logged in -->
    <div v-if="!loggedIn" class="text-center py-20">
      <h2 class="text-2xl font-bold text-slate-700 mb-2">Portfolio Analysis</h2>
      <p class="text-slate-500">Please log in to view your portfolio analysis.</p>
    </div>

    <template v-else>
      <h1 class="text-2xl font-bold text-slate-800 mb-6">Portfolio Analysis</h1>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-20">
        <p class="text-slate-400">Analyzing your portfolio...</p>
      </div>

      <!-- No holdings -->
      <div v-else-if="!analysis" class="text-center py-20">
        <p class="text-slate-500">{{ errorMsg || 'Add stocks to your portfolios to see analysis.' }}</p>
      </div>

      <template v-else>
        <!-- Summary Cards -->
        <section class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
          <div class="bg-white rounded-xl shadow border border-slate-200 p-4 text-center">
            <p class="text-sm text-slate-500">Total Value</p>
            <p class="text-2xl font-bold text-blue-700">${{ formatNum(analysis.summary.totalValue) }}</p>
          </div>
          <div class="bg-white rounded-xl shadow border border-slate-200 p-4 text-center">
            <p class="text-sm text-slate-500">Total Cost</p>
            <p class="text-2xl font-bold text-slate-600">${{ formatNum(analysis.summary.totalCost) }}</p>
          </div>
          <div class="bg-white rounded-xl shadow border border-slate-200 p-4 text-center">
            <p class="text-sm text-slate-500">Total P&L</p>
            <p class="text-2xl font-bold" :class="analysis.summary.totalPnl >= 0 ? 'text-green-600' : 'text-red-600'">
              {{ analysis.summary.totalPnl >= 0 ? '+' : '' }}${{ formatNum(analysis.summary.totalPnl) }}
              <span class="text-sm font-normal block">
                ({{ analysis.summary.totalPnl >= 0 ? '+' : '' }}{{ analysis.summary.totalPnlPercent.toFixed(2) }}%)
              </span>
            </p>
          </div>
          <div class="bg-white rounded-xl shadow border border-slate-200 p-4 text-center">
            <p class="text-sm text-slate-500">Portfolio Grade</p>
            <p class="text-2xl font-bold" :class="gradeColor">
              {{ analysis.grade.portfolio_score }}
              <span class="text-sm font-normal text-slate-400">/ 100</span>
            </p>
          </div>
        </section>

        <!-- Holdings Table -->
        <section class="mb-8">
          <h2 class="text-xl font-semibold text-slate-700 mb-4">Holdings</h2>
          <div class="bg-white rounded-xl shadow border border-slate-200 overflow-x-auto">
            <table class="w-full text-sm">
              <thead>
                <tr class="border-b border-slate-200 text-left text-slate-500">
                  <th class="px-4 py-3">Symbol</th>
                  <th class="px-4 py-3">Name</th>
                  <th class="px-4 py-3 text-right">Shares</th>
                  <th class="px-4 py-3 text-right">Avg Cost</th>
                  <th class="px-4 py-3 text-right">Price</th>
                  <th class="px-4 py-3 text-right">Value</th>
                  <th class="px-4 py-3 text-right">P&L</th>
                  <th class="px-4 py-3 text-right">Alloc</th>
                </tr>
              </thead>
              <tbody>
                <tr
                  v-for="h in analysis.holdings"
                  :key="h.symbol"
                  class="border-b border-slate-100 hover:bg-slate-50"
                >
                  <td class="px-4 py-3 font-semibold text-blue-700">{{ h.symbol }}</td>
                  <td class="px-4 py-3 text-slate-600">{{ h.name }}</td>
                  <td class="px-4 py-3 text-right">{{ h.shares }}</td>
                  <td class="px-4 py-3 text-right">${{ h.averageCost.toFixed(2) }}</td>
                  <td class="px-4 py-3 text-right">${{ h.currentPrice.toFixed(2) }}</td>
                  <td class="px-4 py-3 text-right">${{ formatNum(h.marketValue) }}</td>
                  <td class="px-4 py-3 text-right" :class="h.pnl >= 0 ? 'text-green-600' : 'text-red-600'">
                    {{ h.pnl >= 0 ? '+' : '' }}${{ formatNum(h.pnl) }}
                    <span class="text-xs block">{{ h.pnl >= 0 ? '+' : '' }}{{ h.pnlPercent.toFixed(2) }}%</span>
                  </td>
                  <td class="px-4 py-3 text-right">{{ h.allocation.toFixed(1) }}%</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- Sector Allocation + Grade Side by Side -->
        <section class="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <!-- Sector Allocation -->
          <div class="bg-white rounded-xl shadow border border-slate-200 p-5">
            <h3 class="text-lg font-semibold text-slate-800 mb-4">Sector Allocation</h3>
            <div class="space-y-3">
              <div v-for="s in analysis.sectorBreakdown" :key="s.sector">
                <div class="flex justify-between text-sm mb-1">
                  <span class="text-slate-600">{{ s.sector }}</span>
                  <span class="font-medium text-slate-800">{{ s.percent.toFixed(1) }}%</span>
                </div>
                <div class="w-full bg-slate-100 rounded-full h-2.5">
                  <div
                    class="h-2.5 rounded-full bg-blue-500"
                    :style="{ width: s.percent + '%' }"
                  ></div>
                </div>
              </div>
              <p v-if="!analysis.sectorBreakdown.length" class="text-sm text-slate-400">
                No sector data available.
              </p>
            </div>
          </div>

          <!-- Portfolio Grade -->
          <StockGrading :score="analysis.grade" />
        </section>
      </template>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import StockGrading from '../components/stock_grading.vue'

const loggedIn = ref(false)
const loading = ref(true)
const analysis = ref(null)
const errorMsg = ref('')

const gradeColor = computed(() => {
  if (!analysis.value) return 'text-slate-300'
  const s = analysis.value.grade.portfolio_score
  if (s >= 75) return 'text-green-600'
  if (s >= 50) return 'text-yellow-600'
  if (s >= 25) return 'text-orange-600'
  return 'text-red-600'
})

function formatNum(n) {
  return Math.abs(n) >= 1000
    ? n.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
    : n.toFixed(2)
}

onMounted(async () => {
  const token = localStorage.getItem('token')
  if (!token) {
    loading.value = false
    return
  }
  loggedIn.value = true

  try {
    // 1. Fetch portfolios from Node backend
    const res = await fetch('http://localhost:5000/api/portfolios', {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (!res.ok) throw new Error('Failed to load portfolios')
    const portfolios = await res.json()

    // 2. Collect all holdings across portfolios
    const holdingsMap = {}
    for (const p of portfolios) {
      for (const h of (p.holdings || [])) {
        const symbol = h.symbol || h.stockId
        if (!symbol) continue
        if (holdingsMap[symbol]) {
          // Merge: add shares, weighted average cost
          const existing = holdingsMap[symbol]
          const totalShares = existing.shares + h.shares
          existing.averageCost = (existing.averageCost * existing.shares + h.averageCost * h.shares) / totalShares
          existing.shares = totalShares
        } else {
          holdingsMap[symbol] = {
            symbol: symbol,
            shares: h.shares,
            averageCost: h.averageCost
          }
        }
      }
    }

    const holdings = Object.values(holdingsMap)
    if (!holdings.length) {
      errorMsg.value = 'No holdings found. Add stocks to your portfolios to see analysis.'
      loading.value = false
      return
    }

    // 3. Call Python analysis endpoint
    const token = localStorage.getItem('token')
    const analysisRes = await fetch('http://localhost:8000/grades/analysis', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
      body: JSON.stringify({ holdings })
    })

    if (!analysisRes.ok) {
      const err = await analysisRes.json().catch(() => ({}))
      throw new Error(err.detail || 'Analysis failed')
    }

    analysis.value = await analysisRes.json()
  } catch (err) {
    errorMsg.value = err.message || 'Failed to load analysis.'
  } finally {
    loading.value = false
  }
})
</script>
