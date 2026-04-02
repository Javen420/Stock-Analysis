<template>
  <div class="min-h-screen bg-cream text-charcoal font-body pb-24" style="padding-top: 140px; padding-left: 40px;">

    <!-- Main Content Unboxed -->
    <main class="w-full max-w-[1920px] mx-auto px-6 md:px-12 2xl:px-24 space-y-24">
      
      <div v-if="loading" class="h-64 flex items-center justify-center">
        <div class="w-8 h-8 rounded-full border-t-2 border-clay animate-spin"></div>
      </div>

      <template v-else-if="stockData">
        
        <!-- Header Section -->
        <header class="flex flex-col md:flex-row md:items-end justify-between gap-12">
          <div class="space-y-6">
            <router-link to="/dashboard" class="group inline-flex items-center gap-2 text-charcoal/50 font-mono text-sm uppercase tracking-widest hover:text-charcoal transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="transform group-hover:-translate-x-1 transition-transform"><path d="M19 12H5"/><path d="m12 19-7-7 7-7"/></svg>
              Back to Overview
            </router-link>
            
            <div>
              <div class="flex items-center gap-4 mb-3">
                <h1 class="font-heading font-bold text-6xl md:text-8xl text-charcoal tracking-tighter">{{ stockData.symbol }}</h1>
                <span class="px-3 py-1 bg-charcoal/5 text-charcoal/50 rounded-full font-mono text-xs font-bold">{{ stockData.exchange }}</span>
                <span class="px-3 py-1 bg-moss/10 text-moss rounded-full font-mono text-xs font-bold">{{ stockData.sector }}</span>
              </div>
              <p class="text-charcoal/60 text-2xl font-drama italic">{{ stockData.name }}</p>
            </div>
            
            <p class="font-body text-charcoal/50 text-base leading-relaxed max-w-2xl">
              {{ stockData.description }}
            </p>
          </div>

          <div class="flex flex-col items-end">
            <div class="text-charcoal/40 text-xs font-mono uppercase tracking-widest mb-2">Current Tick</div>
            <div class="text-5xl md:text-7xl font-mono text-charcoal font-bold tracking-tighter">${{ currentPrice }}</div>
            <div class="text-lg font-mono font-medium flex items-center gap-2 justify-end mt-2" :class="priceChange >= 0 ? 'text-emerald-500' : 'text-clay'">
              <svg v-if="priceChange >= 0" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="18 15 12 9 6 15"/></svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
              {{ priceChange >= 0 ? '+' : '' }}{{ priceChange }} ({{ priceChangePercent }}%)
            </div>
          </div>
        </header>

        <!-- Chart Section Unboxed -->
        <div class="space-y-4">
          <div class="font-mono text-xs uppercase tracking-widest text-charcoal/40 border-b border-charcoal/10 pb-4">100-Day Price Action</div>
          <div class="h-[400px] w-full flex items-center justify-center relative overflow-hidden bg-white/50 backdrop-blur-sm shadow-sm rounded-3xl border border-charcoal/5 p-10">
            <!-- Mock Chart SVGs -->
            <svg viewBox="0 0 800 300" class="w-full h-full opacity-80" preserveAspectRatio="none">
              <path d="M 0 200 Q 150 250 300 150 T 600 200 T 800 50" fill="none" stroke="#CC5833" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M 0 300 L 0 200 Q 150 250 300 150 T 600 200 T 800 50 L 800 300 Z" fill="url(#clayGradient)" opacity="0.1" />
              <defs>
                <linearGradient id="clayGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stop-color="#CC5833" />
                  <stop offset="100%" stop-color="transparent" />
                </linearGradient>
              </defs>
            </svg>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-16 md:gap-32">
          
          <!-- Technicals Unboxed -->
          <div class="space-y-12">
            <h3 class="font-heading font-bold text-3xl tracking-tight text-charcoal border-b border-charcoal/10 pb-6">Technical Signal</h3>
            
            <div class="flex items-center gap-12">
              <div>
                <div class="text-charcoal/40 text-[10px] font-mono uppercase tracking-widest mb-3">RSI (14)</div>
                <div class="font-heading text-5xl font-bold" :class="technicals.technicals.rsi > 70 ? 'text-clay' : technicals.technicals.rsi < 30 ? 'text-emerald-500' : 'text-charcoal'">{{ technicals.technicals.rsi }}</div>
              </div>
              <div class="w-px h-16 bg-charcoal/10"></div>
              <div>
                <div class="text-charcoal/40 text-[10px] font-mono uppercase tracking-widest mb-3">MACD Hist</div>
                <div class="font-heading text-5xl font-bold" :class="technicals.technicals.macd.histogram > 0 ? 'text-emerald-500' : 'text-clay'">{{ technicals.technicals.macd.histogram }}</div>
              </div>
              <div class="w-px h-16 bg-charcoal/10"></div>
              <div>
                <div class="text-charcoal/40 text-[10px] font-mono uppercase tracking-widest mb-3">SMA 50</div>
                <div class="font-mono text-4xl text-charcoal font-medium">${{ technicals.technicals.sma50 }}</div>
              </div>
            </div>
            
            <div class="bg-charcoal text-cream p-12 rounded-3xl flex flex-col items-center justify-center text-center mt-12 relative overflow-hidden shadow-2xl">
              <!-- Background abstract -->
               <div class="absolute inset-0 bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-moss/20 to-transparent opacity-50"></div>
              
              <div class="relative z-10 w-full">
                <div class="text-xs text-cream/50 font-mono uppercase tracking-widest mb-4">Total Factor Score</div>
                <div class="font-drama text-8xl text-cream mb-8 leading-none">{{ technicals.scoring.overallScore }}<span class="text-4xl text-cream/30">/100</span></div>
                <div class="flex justify-between items-center w-full max-w-sm mx-auto pt-6 border-t border-cream/10">
                  <div class="text-center">
                    <span class="block text-xs text-cream/50 font-mono uppercase tracking-widest mb-1">Value</span>
                    <span class="font-mono text-xl">{{ technicals.scoring.valueScore }}</span>
                  </div>
                  <div class="text-center">
                    <span class="block text-xs text-cream/50 font-mono uppercase tracking-widest mb-1">Growth</span>
                    <span class="font-mono text-xl">{{ technicals.scoring.growthScore }}</span>
                  </div>
                  <div class="text-center">
                    <span class="block text-xs text-cream/50 font-mono uppercase tracking-widest mb-1">Momentum</span>
                    <span class="font-mono text-xl">{{ technicals.scoring.momentumScore }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Fundamentals Unboxed -->
          <div class="space-y-12">
            <h3 class="font-heading font-bold text-3xl tracking-tight text-charcoal border-b border-charcoal/10 pb-6">Fundamentals</h3>
            
            <div class="space-y-6">
              <div class="flex justify-between items-end border-b border-charcoal/5 pb-4">
                <span class="text-lg text-charcoal/60">P/E Ratio</span>
                <span class="text-2xl font-mono text-charcoal font-medium">{{ technicals.fundamentals.pe }}</span>
              </div>
              <div class="flex justify-between items-end border-b border-charcoal/5 pb-4">
                <span class="text-lg text-charcoal/60">Earnings Per Share (TTM)</span>
                <span class="text-2xl font-mono text-charcoal font-medium">${{ technicals.fundamentals.eps }}</span>
              </div>
              <div class="flex justify-between items-end border-b border-charcoal/5 pb-4">
                <span class="text-lg text-charcoal/60">Profit Margin</span>
                <span class="text-2xl font-mono text-charcoal font-medium">{{ (technicals.fundamentals.profitMargin * 100).toFixed(1) }}%</span>
              </div>
              <div class="flex justify-between items-end border-b border-charcoal/5 pb-4">
                <span class="text-lg text-charcoal/60">Dividend Yield</span>
                <span class="text-2xl font-mono text-charcoal font-medium">{{ (technicals.fundamentals.dividendYield * 100).toFixed(2) }}%</span>
              </div>
              <div class="flex justify-between items-end border-b border-charcoal/5 pb-4">
                <span class="text-lg text-charcoal/60">Return on Equity</span>
                <span class="text-2xl font-mono text-charcoal font-medium">{{ (technicals.fundamentals.roe * 100).toFixed(1) }}%</span>
              </div>
               <div class="flex justify-between items-end border-b border-charcoal/5 pb-4">
                <span class="text-lg text-charcoal/60">Debt to Equity</span>
                <span class="text-2xl font-mono text-charcoal font-medium">{{ technicals.fundamentals.debtToEquity }}</span>
              </div>
            </div>
          </div>
        </div>

      </template>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const symbolParam = computed(() => route.params.symbol.toUpperCase())

const loading = ref(true)
const stockData = ref(null)
const technicals = ref(null)

const currentPrice = ref(0)
const priceChange = ref(0)
const priceChangePercent = ref(0)

onMounted(() => {
  setTimeout(() => {
    stockData.value = {
      symbol: symbolParam.value,
      name: `${symbolParam.value} Corporation`,
      exchange: 'NASDAQ',
      sector: 'Technology',
      description: `${symbolParam.value} Corporation engages in the design, manufacture, and marketing of technical products, software and services worldwide. This data is synthetically pulled from the Python analytics server providing institutional-grade insight.`,
      prices: [
        { date: '2026-04-02', price: 172.50 },
        { date: '2026-04-01', price: 168.20 }
      ]
    }

    currentPrice.value = stockData.value.prices[0].price
    const prevPrice = stockData.value.prices[1].price
    priceChange.value = (currentPrice.value - prevPrice).toFixed(2)
    priceChangePercent.value = ((priceChange.value / prevPrice) * 100).toFixed(2)

    technicals.value = {
      fundamentals: {
        pe: 28.5,
        eps: 6.05,
        pb: 4.2,
        dividendYield: 0.012,
        profitMargin: 0.22,
        debtToEquity: 0.8,
        roe: 0.25
      },
      technicals: {
        rsi: 62.4,
        macd: { macd: 1.25, signal: 0.95, histogram: 0.30 },
        sma50: 158.40
      },
      scoring: {
        valueScore: 18.5,
        growthScore: 22.1,
        momentumScore: 19.8,
        overallScore: 82.4
      }
    }

    loading.value = false
  }, 800)
})
</script>
