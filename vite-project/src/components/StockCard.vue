<!-- maybe just for profile, or if there can be multiple components in one file, then for the whole <applet></applet> -->

<template>
  <div
    class="w-full max-w-sm rounded-2xl shadow-md p-4"
  >
    <div class="mb-2">
      <h2 class="text-xl font-semibold">{{ stock.name }}</h2>
      <p class="text-sm text-gray-500">{{ stock.ticker }}</p>
    </div>

    <div class="space-y-4">
      <div class="text-2xl font-bold">{{ stock.price }}</div>

      <!-- Graph placeholder -->
      <div class="w-full h-32 bg-gray-200 rounded-xl flex items-center justify-center text-gray-500">
        Graph Placeholder
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"

const stock = ref(null)

onMounted(async () => {
  const res = await fetch("http://localhost:8000/stock")
  stock.value = await res.json()
})

</script>

<style scoped>
</style>
