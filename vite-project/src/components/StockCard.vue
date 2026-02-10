<template>
  <div class="bg-white rounded-xl shadow border border-slate-200 p-4">
    <template v-if="loading">
      <div class="animate-pulse space-y-3">
        <div class="h-5 bg-slate-200 rounded w-1/2"></div>
        <div class="h-4 bg-slate-200 rounded w-1/3"></div>
        <div class="h-8 bg-slate-200 rounded w-1/4 mt-2"></div>
        <div class="h-28 bg-slate-100 rounded-lg"></div>
      </div>
    </template>

    <template v-else-if="stock">
      <div class="mb-2">
        <h2 class="text-lg font-semibold text-slate-800">{{ stock.name || symbol }}</h2>
        <p class="text-sm text-slate-500">{{ stock.symbol || symbol }}</p>
      </div>

      <div v-if="latestPrice" class="text-2xl font-bold text-slate-800 mb-3">
        ${{ latestPrice }}
      </div>

      <!-- Mini price chart -->
      <Charts
        v-if="stock.prices && stock.prices.length"
        :prices="stock.prices"
        :height="120"
      />
      <div v-else class="h-28 bg-slate-100 rounded-lg flex items-center justify-center text-sm text-slate-400">
        No price data
      </div>
    </template>

    <template v-else-if="error">
      <div class="text-center py-4">
        <p class="text-sm text-slate-400">{{ error }}</p>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Charts from './Charts.vue'

const props = defineProps({
  symbol: { type: String, required: true }
})

const stock = ref(null)
const loading = ref(true)
const error = ref(null)

const latestPrice = computed(() => {
  if (!stock.value?.prices?.length) return null
  return Number(stock.value.prices[0].price).toFixed(2)
})

onMounted(async () => {
  try {
    const res = await fetch(`http://localhost:8000/stocks/${props.symbol}`)
    if (!res.ok) {
      error.value = `Could not load ${props.symbol}`
      return
    }
    stock.value = await res.json()
  } catch {
    error.value = `Could not load ${props.symbol}`
  } finally {
    loading.value = false
  }
})
</script>
