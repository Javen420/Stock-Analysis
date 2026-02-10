<template>
  <div class="relative w-full max-w-lg mx-auto">
    <div class="flex">
      <input
        v-model="query"
        @keydown.enter="search"
        type="text"
        placeholder="Search by ticker (e.g. AAPL, MSFT)..."
        class="flex-1 px-4 py-2 border border-slate-300 rounded-l-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800"
      />
      <button
        @click="search"
        :disabled="loading"
        class="bg-blue-700 hover:bg-blue-600 text-white px-5 py-2 rounded-r-lg transition-colors disabled:opacity-50"
      >
        {{ loading ? 'Searching...' : 'Search' }}
      </button>
    </div>

    <p v-if="error" class="text-red-600 text-sm mt-2">{{ error }}</p>

    <!-- Search Result -->
    <div
      v-if="result"
      class="mt-4 bg-white border border-slate-200 rounded-xl shadow p-4 text-left"
    >
      <div class="flex items-center justify-between mb-2">
        <div>
          <h3 class="text-lg font-semibold text-blue-800">{{ result.symbol }}</h3>
          <p class="text-sm text-slate-500">{{ result.name }}</p>
        </div>
        <span v-if="latestPrice" class="text-xl font-bold text-slate-800">
          ${{ latestPrice }}
        </span>
      </div>

      <!-- Price history mini-list -->
      <div v-if="result.prices && result.prices.length" class="mt-3">
        <h4 class="text-sm font-medium text-slate-600 mb-2">Recent Prices</h4>
        <div class="max-h-40 overflow-y-auto space-y-1">
          <div
            v-for="(p, i) in result.prices.slice(0, 10)"
            :key="i"
            class="flex justify-between text-sm text-slate-600 px-2 py-1 rounded hover:bg-slate-50"
          >
            <span>{{ p.date }}</span>
            <span class="font-medium">${{ Number(p.price).toFixed(2) }}</span>
          </div>
        </div>
      </div>

      <button
        @click="$emit('select', result.symbol)"
        class="mt-3 bg-blue-700 hover:bg-blue-600 text-white text-sm px-4 py-1.5 rounded transition-colors"
      >
        View Details
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const emit = defineEmits(['select'])

const query = ref('')
const result = ref(null)
const loading = ref(false)
const error = ref(null)

const latestPrice = computed(() => {
  if (!result.value?.prices?.length) return null
  return Number(result.value.prices[0].price).toFixed(2)
})

async function search() {
  const symbol = query.value.trim().toUpperCase()
  if (!symbol) return

  error.value = null
  result.value = null
  loading.value = true

  try {
    const res = await fetch(`http://localhost:8000/stocks/${symbol}`)
    if (!res.ok) {
      const data = await res.json().catch(() => ({}))
      error.value = data.detail || `Ticker "${symbol}" not found`
      return
    }
    result.value = await res.json()
  } catch {
    error.value = 'Could not connect to stock API. Make sure the Python backend is running.'
  } finally {
    loading.value = false
  }
}
</script>
