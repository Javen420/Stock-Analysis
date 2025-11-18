<script setup>
import NavBar from './components/NavBar.vue'
</script>

<template>
  <div>
    <NavBar />
    <router-view />
  </div>
</template>

<style scoped>
/* Optional global styles for App.vue */
body {
  margin: 0;
  font-family: Arial, sans-serif;
}
</style>
