<template>
  <div class="bg-white rounded-xl shadow border border-slate-200 p-5">
    <h3 class="text-lg font-semibold text-slate-800 mb-4">Portfolio Grade</h3>

    <template v-if="score">
      <!-- Overall Score -->
      <div class="text-center mb-5">
        <div
          class="inline-flex items-center justify-center w-20 h-20 rounded-full text-2xl font-bold"
          :class="scoreColor"
        >
          {{ score.portfolio_score }}
        </div>
        <p class="text-sm text-slate-500 mt-1">/ 100</p>
      </div>

      <!-- Score Breakdown -->
      <div class="space-y-3">
        <ScoreBar label="Stock Quality" :value="score.stock_component" :max="50" />
        <ScoreBar label="Sharpe Ratio" :value="score.sharpe_component" :max="25" />
        <ScoreBar label="Diversification" :value="score.diversification_component" :max="15" />
        <ScoreBar label="Risk" :value="score.risk_component" :max="10" />
      </div>
    </template>

    <template v-else>
      <p class="text-sm text-slate-400 text-center py-4">
        No grading data available. Add stocks to a portfolio to see your grade.
      </p>
    </template>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  score: { type: Object, default: null }
})

const scoreColor = computed(() => {
  if (!props.score) return 'bg-slate-100 text-slate-400'
  const s = props.score.portfolio_score
  if (s >= 75) return 'bg-green-100 text-green-700'
  if (s >= 50) return 'bg-yellow-100 text-yellow-700'
  if (s >= 25) return 'bg-orange-100 text-orange-700'
  return 'bg-red-100 text-red-700'
})

// Inline sub-component for score bars
const ScoreBar = {
  props: {
    label: String,
    value: Number,
    max: Number
  },
  template: `
    <div>
      <div class="flex justify-between text-sm mb-1">
        <span class="text-slate-600">{{ label }}</span>
        <span class="font-medium text-slate-800">{{ value }} / {{ max }}</span>
      </div>
      <div class="w-full bg-slate-100 rounded-full h-2">
        <div
          class="h-2 rounded-full transition-all"
          :class="value / max >= 0.6 ? 'bg-blue-500' : 'bg-amber-400'"
          :style="{ width: (value / max * 100) + '%' }"
        ></div>
      </div>
    </div>
  `
}
</script>
