<template>
  <div class="max-w-5xl mx-auto px-4 py-8">
    <!-- Not logged in -->
    <div v-if="!loggedIn" class="text-center py-20">
      <h2 class="text-2xl font-bold text-slate-700 mb-2">Profile</h2>
      <p class="text-slate-500">Please log in to view your profile.</p>
    </div>

    <template v-else>
      <!-- Profile Header -->
      <section class="mb-8">
        <h2 class="text-2xl font-bold text-slate-800 mb-1">{{ user.username }}</h2>
        <p class="text-sm text-slate-500">{{ user.email }}</p>
      </section>

      <!-- Stats Cards -->
      <section class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
        <div class="bg-white rounded-xl shadow border border-slate-200 p-4 text-center">
          <p class="text-sm text-slate-500">Portfolios</p>
          <p class="text-2xl font-bold text-blue-700">{{ portfolios.length }}</p>
        </div>
        <div class="bg-white rounded-xl shadow border border-slate-200 p-4 text-center">
          <p class="text-sm text-slate-500">Total Holdings</p>
          <p class="text-2xl font-bold text-blue-700">{{ totalHoldings }}</p>
        </div>
        <div class="bg-white rounded-xl shadow border border-slate-200 p-4 text-center">
          <p class="text-sm text-slate-500">Watchlist</p>
          <p class="text-2xl font-bold text-blue-700">{{ watchlistCount }}</p>
        </div>
        <div class="bg-white rounded-xl shadow border border-slate-200 p-4 text-center">
          <p class="text-sm text-slate-500">Portfolio Score</p>
          <p class="text-2xl font-bold" :class="gradeScore ? 'text-blue-700' : 'text-slate-300'">
            {{ gradeScore ?? '-' }}
          </p>
        </div>
      </section>

      <!-- Portfolios Overview -->
      <section class="mb-8">
        <h3 class="text-xl font-semibold text-slate-700 mb-4">Portfolios</h3>
        <div v-if="portfolios.length" class="space-y-3">
          <div
            v-for="portfolio in portfolios"
            :key="portfolio._id"
            class="bg-white rounded-xl shadow border border-slate-200 p-4"
          >
            <div class="flex items-center justify-between mb-2">
              <h4 class="font-semibold text-blue-700">{{ portfolio.name }}</h4>
              <span class="text-sm text-slate-400">
                {{ portfolio.holdings?.length || 0 }} stocks
              </span>
            </div>
            <p class="text-sm text-slate-500">{{ portfolio.description || 'No description' }}</p>
          </div>
        </div>
        <p v-else class="text-sm text-slate-400">No portfolios created yet.</p>
      </section>

      <!-- Portfolio Grading -->
      <section>
        <StockGrading :score="gradeData" />
      </section>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import StockGrading from '../components/stock_grading.vue'

const loggedIn = ref(false)
const user = ref({})
const portfolios = ref([])
const watchlistCount = ref(0)
const gradeData = ref(null)

const totalHoldings = computed(() => {
  return portfolios.value.reduce((sum, p) => sum + (p.holdings?.length || 0), 0)
})

const gradeScore = computed(() => {
  return gradeData.value?.portfolio_score ?? null
})

onMounted(async () => {
  const token = localStorage.getItem('token')
  const stored = JSON.parse(localStorage.getItem('user') || '{}')
  if (!token || !stored.id) return

  loggedIn.value = true
  user.value = stored

  const headers = { Authorization: `Bearer ${token}` }

  // Fetch portfolios
  try {
    const res = await fetch('http://localhost:5000/api/portfolios', { headers })
    if (res.ok) {
      portfolios.value = await res.json()
    }
  } catch {
    // endpoint not ready yet
  }

  // Fetch watchlist count
  try {
    const res = await fetch(`http://localhost:5000/api/users/${stored.id}/watchlist`, { headers })
    if (res.ok) {
      const data = await res.json()
      watchlistCount.value = data.watchlist?.length || 0
    }
  } catch {
    // endpoint not ready yet
  }

  // Fetch portfolio grading
  try {
    const res = await fetch('http://localhost:8000/grades/')
    if (res.ok) {
      const data = await res.json()
      if (data.portfolio_score !== undefined) {
        gradeData.value = data
      }
    }
  } catch {
    // endpoint not ready yet
  }
})
</script>
