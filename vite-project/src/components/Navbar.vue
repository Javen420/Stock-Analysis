<template>
  <nav class="navbar">
    <div class="logo">My App</div>
    <div class="links">
      <router-link to="/">Home</router-link>
      <router-link to="/about">About</router-link>
      <router-link to="/contact">Contact Us</router-link>
      <router-link to="/profile">Profile</router-link>
      <router-link to="/login">Login</router-link>
    </div>
  </nav>
</template>

<script>
export default {
  name: "NavBar",
}
</script>

<style scoped>
.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #1e40af;
  color: white;
}

.logo {
  font-size: 1.5rem;
  font-weight: bold;
}

.links a,
.links router-link {
  margin-left: 1rem;
  text-decoration: none;
  color: white;
  font-weight: 500;
}

.links a:hover,
.links router-link:hover {
  color: #cbd5e1;
}
</style>
