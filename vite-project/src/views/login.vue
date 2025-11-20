<template>
  <div class="login-form">
    <div class="form-group">
      <label for="username">Username:</label>
      <input type="text" id="username" v-model="username" />
    </div>

    <div class="form-group">
      <label for="password">Password:</label>
      <input type="password" id="password" v-model="password" />
    </div>

    <button @click="login">Login</button>
  </div>
</template>
<!-- might want to make this a pop up or use oauth? -->
<script setup>
import { ref } from 'vue'

// Reactive variables for the input fields
const username = ref('')
const password = ref('')

// Example login function
const login = () => {
  console.log('Username:', username.value)
  console.log('Password:', password.value)
  // Here you would call your backend API to authenticate the user
}
</script>

<style scoped>
.login-form {
  display: flex;
  flex-direction: column;
  max-width: 300px;
  margin: 2rem auto;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

input {
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 0.5rem;
  background-color: #1e40af;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #3b82f6;
}
</style>
