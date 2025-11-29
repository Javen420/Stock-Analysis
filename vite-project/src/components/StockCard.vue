<!-- maybe just for profile, or if there can be multiple components in one file, then for the whole <applet></applet> -->

<template>
  <div
    class="w-full max-w-sm rounded-2xl shadow-md p-4"
  >
    <div class="mb-2">
      <h2 class="text-xl font-semibold">{{ name }}</h2>
      <p class="text-sm text-gray-500">{{ ticker }}</p>
    </div>

    <div class="space-y-4">
      <div class="text-2xl font-bold">{{ price }}</div>

      <!-- Graph placeholder -->
      <div class="w-full h-32 bg-gray-200 rounded-xl flex items-center justify-center text-gray-500">
        Graph Placeholder
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  name: { type: String, default: "Apple Inc." },
  ticker: { type: String, default: "AAPL" },
  price: { type: String, default: "$182.45" }
});
</script>

<style scoped>
</style>
