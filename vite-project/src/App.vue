<template>
  <div class="relative min-h-screen bg-cream text-charcoal font-body">
    <NavBar />
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup>
import NavBar from './components/NavBar.vue'
</script>
