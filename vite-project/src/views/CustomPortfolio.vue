<template>
  <div class="min-h-screen bg-cream text-charcoal font-body pb-24" style="padding-top: 140px; padding-left: 40px;">
    <!-- Main Content Unboxed -->
    <main class="w-full max-w-[1920px] mx-auto px-6 md:px-12 2xl:px-24 space-y-24">
      
      <header class="text-center max-w-2xl mx-auto">
        <span class="font-mono text-xs text-clay uppercase tracking-widest flex items-center justify-center gap-3 mb-6">
          <span class="inline-block w-6 h-px bg-clay"></span>
          Simulator
          <span class="inline-block w-6 h-px bg-clay"></span>
        </span>
        <h1 class="font-heading font-bold text-5xl md:text-7xl text-charcoal tracking-tight mb-6">Build & Stress Test.</h1>
        <p class="text-charcoal/60 text-lg leading-relaxed">
          Queue up assets, define basis, and preview proprietary grade scores before committing institutional capital.
        </p>
      </header>

      <!-- Builder Form Full Width -->
      <div class="bg-white/50 backdrop-blur-md border border-charcoal/5 shadow-xl rounded-[2rem] p-8 md:p-12 max-w-4xl mx-auto">
        
        <div class="grid grid-cols-1 md:grid-cols-12 gap-6 mb-8 items-end">
          <div class="md:col-span-4 space-y-3">
            <label class="font-mono text-xs text-charcoal/50 uppercase tracking-widest font-bold">Ticker Symbol</label>
            <input v-model="form.symbol" @keyup.enter="addAsset" type="text" placeholder="e.g. AAPL" class="w-full bg-white border border-charcoal/10 rounded-2xl px-6 py-4 text-charcoal font-mono outline-none focus:border-clay focus:ring-2 focus:ring-clay/20 transition-all uppercase placeholder-charcoal/20 font-medium">
          </div>
          <div class="md:col-span-3 space-y-3">
            <label class="font-mono text-xs text-charcoal/50 uppercase tracking-widest font-bold">Shares</label>
            <input v-model.number="form.shares" @keyup.enter="addAsset" type="number" min="0" step="any" placeholder="100" class="w-full bg-white border border-charcoal/10 rounded-2xl px-6 py-4 text-charcoal font-mono outline-none focus:border-clay focus:ring-2 focus:ring-clay/20 transition-all placeholder-charcoal/20 font-medium">
          </div>
          <div class="md:col-span-3 space-y-3">
            <label class="font-mono text-xs text-charcoal/50 uppercase tracking-widest font-bold">Avg Cost</label>
            <input v-model.number="form.cost" @keyup.enter="addAsset" type="number" min="0" step="any" placeholder="150.00" class="w-full bg-white border border-charcoal/10 rounded-2xl px-6 py-4 text-charcoal font-mono outline-none focus:border-clay focus:ring-2 focus:ring-clay/20 transition-all placeholder-charcoal/20 font-medium">
          </div>
          <div class="md:col-span-2 flex justify-end pb-1">
            <button @click="addAsset" class="w-full h-14 bg-charcoal text-cream rounded-2xl font-heading font-bold text-sm hover:bg-charcoal/80 transition-colors flex items-center justify-center gap-2 shadow-lg" :disabled="!isValid" :class="{'opacity-50 cursor-not-allowed': !isValid}">
              Add
            </button>
          </div>
        </div>
      </div>

      <!-- Simulated Holdings UNBOXED Table -->
      <div v-if="holdings.length > 0" class="space-y-8 animate-fade-in">
        <div class="flex justify-between items-end border-b border-charcoal/10 pb-6">
          <div>
            <h3 class="font-heading font-bold text-3xl text-charcoal tracking-tight">Target Allocation</h3>
            <p class="text-sm text-charcoal/50 font-mono mt-3 uppercase tracking-widest">Total Capital Required: <span class="font-bold text-charcoal">${{ totalCostBasis }}</span></p>
          </div>
          
          <button @click="savePortfolio" class="bg-moss hover:bg-moss-light text-cream px-8 py-3 rounded-full font-heading font-bold shadow-md hover:shadow-xl transition-all duration-300 flex items-center gap-2">
            <span v-if="saving" class="w-4 h-4 rounded-full border-t border-cream animate-spin"></span>
            <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>
            {{ saving ? 'Generating Grade...' : 'Commit Targets' }}
          </button>
        </div>
        
        <div class="overflow-x-auto">
          <table class="w-full text-left">
            <thead>
              <tr class="text-charcoal/40 font-mono text-xs uppercase tracking-widest border-b border-charcoal/5">
                <th class="py-6 px-4 font-normal">Asset</th>
                <th class="py-6 px-4 font-normal text-right">Shares</th>
                <th class="py-6 px-4 font-normal text-right">Cost/Share</th>
                <th class="py-6 px-4 font-normal text-right">Total Position</th>
                <th class="py-6 px-4 font-normal text-right">Target Wgt</th>
                <th class="py-6 px-4 font-normal text-center"></th>
              </tr>
            </thead>
            <tbody class="divide-y divide-charcoal/5">
              <tr v-for="(h, index) in holdings" :key="index" class="hover:bg-charcoal/5 transition-colors">
                <td class="py-6 px-4 font-bold text-xl text-charcoal">{{ h.symbol }}</td>
                <td class="py-6 px-4 font-mono text-right text-charcoal font-medium">{{ h.shares }}</td>
                <td class="py-6 px-4 font-mono text-right text-charcoal/60">${{ formatCurrency(h.cost) }}</td>
                <td class="py-6 px-4 font-mono text-right text-charcoal font-bold">${{ formatCurrency(h.shares * h.cost) }}</td>
                <td class="py-6 px-4 font-mono text-right text-emerald-600 font-bold tracking-widest">{{ ((h.shares * h.cost) / totalCostRaw * 100).toFixed(1) }}%</td>
                <td class="py-6 px-4 text-center">
                  <button @click="removeAsset(index)" class="text-clay hover:opacity-70 transition-opacity p-2" title="Remove">
                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const form = ref({
  symbol: '',
  shares: null,
  cost: null
})

const holdings = ref([])
const saving = ref(false)

const isValid = computed(() => {
  return form.value.symbol.trim() !== '' && 
         form.value.shares > 0 && 
         form.value.cost > 0
})

const totalCostRaw = computed(() => {
  return holdings.value.reduce((acc, curr) => acc + (curr.shares * curr.cost), 0)
})

const totalCostBasis = computed(() => {
  return formatCurrency(totalCostRaw.value)
})

function addAsset() {
  if (!isValid.value) return
  
  holdings.value.push({
    symbol: form.value.symbol.toUpperCase().trim(),
    shares: parseFloat(form.value.shares),
    cost: parseFloat(form.value.cost)
  })

  form.value.symbol = ''
  form.value.shares = null
  form.value.cost = null
}

function removeAsset(index) {
  holdings.value.splice(index, 1)
}

function savePortfolio() {
  saving.value = true
  setTimeout(() => {
    saving.value = false
    router.push('/dashboard')
  }, 1000)
}

function formatCurrency(val) {
  return val.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}
</script>
