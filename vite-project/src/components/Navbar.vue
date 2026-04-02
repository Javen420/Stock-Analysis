<template>
  <nav class="fixed top-0 w-full z-50 transition-all duration-300" :class="[
    scrolled ? 'bg-cream/90 backdrop-blur-md border-b border-charcoal/5 py-10' : 'bg-transparent py-16'
  ]">
    <div class="w-full max-w-[1920px] mx-auto px-6 md:px-12 2xl:px-24 flex items-center justify-between">
      <!-- Logo -->
      <router-link to="/" class="flex items-center gap-3 group">
        <div class="w-6 h-6 bg-clay rounded-sm transform group-hover:rotate-12 transition-transform duration-500"></div>
        <span class="font-heading font-bold text-xl text-charcoal tracking-tight">Quantalyze</span>
      </router-link>

      <!-- Desktop Links -->
      <div class="hidden md:flex items-center gap-8 font-mono text-xs uppercase tracking-widest text-charcoal/60">
        <router-link to="/features" class="hover:text-clay transition-colors">Features</router-link>
        <router-link to="/philosophy" class="hover:text-clay transition-colors">Philosophy</router-link>
        <router-link to="/protocol" class="hover:text-clay transition-colors">Protocol</router-link>
        <div class="w-px h-4 bg-charcoal/20"></div>
        <router-link to="/dashboard" class="hover:text-moss transition-colors font-bold text-charcoal">Dashboard</router-link>
        <router-link to="/portfolio/new" class="hover:text-moss transition-colors font-bold text-charcoal">Simulate</router-link>
      </div>

      <!-- Mobile Menu Toggle -->
      <button class="md:hidden text-charcoal" @click="mobileMenuOpen = !mobileMenuOpen">
        <svg v-if="!mobileMenuOpen" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/></svg>
        <svg v-else xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/></svg>
      </button>
    </div>

    <!-- Mobile Dropdown -->
    <div v-show="mobileMenuOpen" class="md:hidden absolute top-full left-0 w-full bg-cream border-b border-charcoal/10 py-6 px-6 flex flex-col gap-6 shadow-xl font-mono text-sm uppercase tracking-widest text-charcoal/80">
      <router-link to="/features" @click="mobileMenuOpen = false">Features</router-link>
      <router-link to="/philosophy" @click="mobileMenuOpen = false">Philosophy</router-link>
      <router-link to="/protocol" @click="mobileMenuOpen = false">Protocol</router-link>
      <div class="w-full h-px bg-charcoal/10 my-2"></div>
      <router-link to="/dashboard" class="text-moss font-bold" @click="mobileMenuOpen = false">Dashboard</router-link>
      <router-link to="/portfolio/new" class="text-moss font-bold" @click="mobileMenuOpen = false">Simulate</router-link>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const scrolled = ref(false)
const mobileMenuOpen = ref(false)

const handleScroll = () => {
  scrolled.value = window.scrollY > 20
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>
