<template>
  <svg
    :viewBox="`0 0 ${width} ${height}`"
    :width="width"
    :height="height"
    class="w-full rounded-lg bg-slate-50"
    preserveAspectRatio="none"
  >
    <!-- Area fill -->
    <path
      v-if="areaPath"
      :d="areaPath"
      :fill="trending >= 0 ? '#dbeafe' : '#fee2e2'"
      opacity="0.5"
    />
    <!-- Line -->
    <polyline
      v-if="points.length"
      :points="pointsStr"
      fill="none"
      :stroke="trending >= 0 ? '#2563eb' : '#dc2626'"
      stroke-width="2"
      stroke-linejoin="round"
      stroke-linecap="round"
    />
  </svg>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  prices: { type: Array, required: true },
  width: { type: Number, default: 300 },
  height: { type: Number, default: 120 }
})

const padding = 4

// Prices come sorted newest-first from the API, reverse for chart (left=oldest)
const sortedPrices = computed(() => {
  return [...props.prices].reverse().map(p => Number(p.price))
})

const points = computed(() => {
  const vals = sortedPrices.value
  if (vals.length < 2) return []

  const min = Math.min(...vals)
  const max = Math.max(...vals)
  const range = max - min || 1

  const usableW = props.width - padding * 2
  const usableH = props.height - padding * 2
  const step = usableW / (vals.length - 1)

  return vals.map((v, i) => ({
    x: padding + i * step,
    y: padding + usableH - ((v - min) / range) * usableH
  }))
})

const pointsStr = computed(() => {
  return points.value.map(p => `${p.x},${p.y}`).join(' ')
})

const areaPath = computed(() => {
  if (points.value.length < 2) return ''
  const pts = points.value
  const first = pts[0]
  const last = pts[pts.length - 1]
  let d = `M ${first.x},${first.y}`
  for (let i = 1; i < pts.length; i++) {
    d += ` L ${pts[i].x},${pts[i].y}`
  }
  d += ` L ${last.x},${props.height} L ${first.x},${props.height} Z`
  return d
})

const trending = computed(() => {
  const vals = sortedPrices.value
  if (vals.length < 2) return 0
  return vals[vals.length - 1] - vals[0]
})
</script>
