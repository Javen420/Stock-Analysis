<template>
  <div class="landing-page">
    <h1>Welcome to the Landing Page</h1>
    <p>This is a minimal working Vue 3 project with a Navbar.</p>
  </div>
</template>

<script setup>
</script>
<!-- dk what to put here, maybe popular stocks + abit of profile, if logged in -->
<style scoped>
.landing-page {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  text-align: center;
  padding: 2rem;
}

.landing-page h1 {
  font-size: 3rem;
  color: #1e40af;
}

.landing-page p {
  font-size: 1.2rem;
  margin-top: 1rem;
}
</style>
