<template>
  <div class="min-h-screen bg-cream text-charcoal font-body pb-24" style="padding-top: 140px; padding-left: 40px;">
    <main class="w-full max-w-[1920px] mx-auto px-6 md:px-12 2xl:px-24 space-y-24">
        
      <!-- Header -->
      <header class="flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div>
          <span class="font-mono text-xs text-moss uppercase tracking-widest flex items-center gap-3 mb-4">
            <span class="inline-block w-6 h-px bg-moss"></span>
            Portfolio Analysis
          </span>
          <h1 class="font-heading font-bold text-5xl md:text-7xl text-charcoal tracking-tight mb-4">Overview.</h1>
          <p class="text-charcoal/50 text-lg md:text-xl max-w-2xl leading-relaxed">Performance metrics and proprietary conviction scoring distributed across a clean environment.</p>
        </div>
        <div class="flex items-center gap-3">
          <span class="px-3 py-1.5 bg-emerald-500/10 text-emerald-600 rounded-full font-mono text-xs uppercase tracking-wider flex items-center gap-2 font-semibold">
            <span class="w-2 h-2 bg-emerald-500 rounded-full animate-pulse"></span> Live Sync
          </span>
        </div>
      </header>

      <!-- Loading State -->
      <div v-if="loading" class="h-64 flex items-center justify-center">
        <div class="w-8 h-8 relative">
          <div class="absolute inset-0 rounded-full border-t-2 border-clay animate-spin"></div>
        </div>
      </div>

      <template v-else>
        <!-- Top KPI Unboxed -->
        <div class="grid grid-cols-1 md:grid-cols-12 gap-8 md:gap-16 items-end">
          
          <!-- Grade -->
          <div class="col-span-1 md:col-span-3">
            <div class="text-charcoal/40 text-xs font-mono uppercase tracking-widest mb-4">Proprietary Q-Score</div>
            <div class="text-7xl md:text-8xl font-drama text-moss leading-none mb-6 tracking-tighter">{{ analysis.grade.portfolio_score }}</div>
            <div class="w-full bg-charcoal/5 h-2 mx-auto overflow-hidden">
              <div class="h-full bg-moss" :style="{ width: `${analysis.grade.portfolio_score}%` }"></div>
            </div>
          </div>
          
          <!-- Value -->
          <div class="col-span-1 md:col-span-4 md:border-l md:border-charcoal/10 md:pl-16">
            <div class="text-charcoal/40 text-xs font-mono uppercase tracking-widest mb-4">Total Value</div>
            <div class="text-4xl md:text-5xl font-heading font-bold text-charcoal tracking-tight">${{ formatNumber(analysis.summary.totalValue) }}</div>
            <div class="mt-4 flex flex-col gap-1 text-sm font-mono text-charcoal/40">
              <span>Cost Basis: ${{ formatNumber(analysis.summary.totalCost) }}</span>
            </div>
          </div>

          <!-- Return -->
          <div class="col-span-1 md:col-span-5 md:border-l md:border-charcoal/10 md:pl-16">
            <div class="text-charcoal/40 text-xs font-mono uppercase tracking-widest mb-4">Total Return</div>
            <div class="flex items-baseline gap-4">
              <div class="text-4xl md:text-5xl font-heading font-bold tracking-tight" :class="analysis.summary.totalPnl >= 0 ? 'text-emerald-500' : 'text-clay'">
                {{ analysis.summary.totalPnl >= 0 ? '+' : '' }}${{ formatNumber(analysis.summary.totalPnl) }}
              </div>
              <div class="text-xl font-mono font-medium" :class="analysis.summary.totalPnlPercent >= 0 ? 'text-emerald-500' : 'text-clay'">
                {{ analysis.summary.totalPnlPercent >= 0 ? '+' : '' }}{{ analysis.summary.totalPnlPercent }}%
              </div>
            </div>
          </div>
        </div>

        <!-- Chart & Sector Breakdown UNBOXED -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-16 md:gap-32 items-start py-8">
          
          <!-- Sector Allocation -->
          <div class="space-y-8">
            <h3 class="font-heading font-bold text-3xl tracking-tight text-charcoal border-b border-charcoal/10 pb-6">Allocations</h3>
            <div class="space-y-8">
              <div v-for="sector in analysis.sectorBreakdown" :key="sector.sector">
                <div class="flex justify-between text-base mb-2">
                  <span class="text-charcoal/80 font-medium">{{ sector.sector }}</span>
                  <span class="font-mono text-charcoal/50">{{ sector.percent }}%</span>
                </div>
                <div class="w-full bg-charcoal/5 h-2 overflow-hidden">
                  <div class="h-full bg-clay transition-all duration-1000" :style="{ width: `${sector.percent}%` }"></div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Component Grade Details -->
          <div class="space-y-8">
            <h3 class="font-heading font-bold text-3xl tracking-tight text-charcoal border-b border-charcoal/10 pb-6">Score Composition</h3>
            <div class="space-y-6">
              <div class="flex justify-between items-center text-lg">
                <span class="text-charcoal/70">Stock DNA (Max 50)</span>
                <span class="font-mono font-bold text-charcoal">{{ analysis.grade.stock_component }}</span>
              </div>
              <div class="flex justify-between items-center text-lg">
                <span class="text-charcoal/70">Sharpe Volatility (Max 25)</span>
                <span class="font-mono font-bold text-charcoal">{{ analysis.grade.sharpe_component }}</span>
              </div>
              <div class="flex justify-between items-center text-lg">
                <span class="text-charcoal/70">Diversification (Max 15)</span>
                <span class="font-mono font-bold text-charcoal">{{ analysis.grade.diversification_component }}</span>
              </div>
              <div class="flex justify-between items-center text-lg pt-6 border-t border-charcoal/5">
                <span class="text-charcoal/70">Risk Profile (Max 10)</span>
                <span class="font-mono font-bold text-charcoal">{{ analysis.grade.risk_component }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Holdings Table UNBOXED -->
        <div class="pt-8 space-y-8">
          <div class="flex items-end justify-between border-b border-charcoal/10 pb-6">
            <h3 class="font-heading font-bold text-3xl tracking-tight">Current Holdings</h3>
            <router-link to="/portfolio/new" class="text-sm font-bold tracking-wider text-clay hover:text-clay/80 uppercase">Manage Simulator</router-link>
          </div>
          
          <div class="overflow-x-auto">
            <table class="w-full text-left">
              <thead>
                <tr class="text-charcoal/40 font-mono text-xs uppercase tracking-widest border-b border-charcoal/5">
                  <th class="py-6 pr-6 font-normal">Asset</th>
                  <th class="py-6 px-6 font-normal hidden md:table-cell">Sector</th>
                  <th class="py-6 px-6 font-normal text-right">Shares</th>
                  <th class="py-6 px-6 font-normal text-right">Avg Cost</th>
                  <th class="py-6 px-6 font-normal text-right">Price</th>
                  <th class="py-6 px-6 font-normal text-right">Return</th>
                  <th class="py-6 pl-6 font-normal text-center">Action</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-charcoal/5">
                <tr v-for="holding in analysis.holdings" :key="holding.symbol" class="group">
                  <td class="py-6 pr-6">
                    <div class="font-bold text-lg flex items-center gap-2 text-charcoal group-hover:text-moss transition-colors">
                      <router-link :to="`/stock/${holding.symbol}`">{{ holding.symbol }}</router-link>
                    </div>
                    <div class="text-sm text-charcoal/50 hidden md:block mt-1">{{ holding.name }}</div>
                  </td>
                  <td class="py-6 px-6 text-charcoal/60 hidden md:table-cell">{{ holding.sector }}</td>
                  <td class="py-6 px-6 font-mono text-right text-charcoal">{{ holding.shares }}</td>
                  <td class="py-6 px-6 font-mono text-right text-charcoal/50">${{ holding.averageCost }}</td>
                  <td class="py-6 px-6 font-mono text-right font-medium">${{ holding.currentPrice }}</td>
                  <td class="py-6 px-6 text-right font-mono font-medium" :class="holding.pnlPercent >= 0 ? 'text-emerald-500' : 'text-clay'">
                    {{ holding.pnlPercent >= 0 ? '+' : '' }}{{ holding.pnlPercent }}%
                  </td>
                  <td class="py-6 pl-6 text-center">
                    <router-link :to="`/stock/${holding.symbol}`" class="text-moss hover:bg-moss/10 px-4 py-2 rounded-full text-xs font-mono font-bold transition-colors uppercase tracking-wider">
                      Analyze
                    </router-link>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </template>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const loading = ref(true)
const analysis = ref(null)

// Mock Data structure based on the FastAPI response contract.
const mockAnalysisData = {
  "summary": {
    "totalValue": 124530.50,
    "totalCost": 105200.00,
    "totalPnl": 19330.50,
    "totalPnlPercent": 18.37,
    "holdingsCount": 4
  },
  "holdings": [
    {
      "symbol": "AAPL",
      "name": "Apple Inc.",
      "sector": "Technology",
      "shares": 150,
      "averageCost": 145.20,
      "currentPrice": 172.50,
      "marketValue": 25875.00,
      "costBasis": 21780.00,
      "pnl": 4095.00,
      "pnlPercent": 18.81,
      "allocation": 20.78
    },
    {
      "symbol": "MSFT",
      "name": "Microsoft Corp.",
      "sector": "Technology",
      "shares": 85,
      "averageCost": 310.50,
      "currentPrice": 412.30,
      "marketValue": 35045.50,
      "costBasis": 26392.50,
      "pnl": 8653.00,
      "pnlPercent": 32.78,
      "allocation": 28.14
    },
    {
      "symbol": "JNJ",
      "name": "Johnson & Johnson",
      "sector": "Healthcare",
      "shares": 200,
      "averageCost": 155.80,
      "currentPrice": 160.20,
      "marketValue": 32040.00,
      "costBasis": 31160.00,
      "pnl": 880.00,
      "pnlPercent": 2.82,
      "allocation": 25.73
    },
    {
      "symbol": "JPM",
      "name": "JPMorgan Chase & Co.",
      "sector": "Financial Services",
      "shares": 160,
      "averageCost": 142.10,
      "currentPrice": 197.31,
      "marketValue": 31569.60,
      "costBasis": 22736.00,
      "pnl": 8833.60,
      "pnlPercent": 38.85,
      "allocation": 25.35
    }
  ],
  "sectorBreakdown": [
    { "sector": "Technology", "value": 60920.50, "percent": 48.92 },
    { "sector": "Healthcare", "value": 32040.00, "percent": 25.73 },
    { "sector": "Financial Services", "value": 31569.60, "percent": 25.35 }
  ],
  "grade": {
    "portfolio_score": 82.4,
    "stock_component": 42.1,
    "sharpe_component": 18.5,
    "diversification_component": 12.8,
    "risk_component": 9.0
  }
}

onMounted(() => {
  setTimeout(() => {
    analysis.value = mockAnalysisData
    loading.value = false
  }, 800)
})

function formatNumber(num) {
  return num.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}
</script>
