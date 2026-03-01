<template>
  <nav class="bg-blue-800 text-white px-6 py-3 flex items-center justify-between shadow-md">
    <router-link to="/" class="text-xl font-bold tracking-wide hover:text-blue-200">
      StockFinder
    </router-link>

    <div class="flex items-center gap-4">
      <router-link to="/" class="hover:text-blue-200 transition-colors">Home</router-link>
      <router-link v-if="loggedIn" to="/my-stocks" class="hover:text-blue-200 transition-colors">My Stocks</router-link>
      <router-link v-if="loggedIn" to="/portfolio-analysis" class="hover:text-blue-200 transition-colors">Analysis</router-link>
      <router-link v-if="loggedIn" to="/profile" class="hover:text-blue-200 transition-colors">Profile</router-link>

      <template v-if="loggedIn">
        <span class="text-blue-200 text-sm">{{ username }}</span>
        <button
          @click="logout"
          class="bg-blue-600 hover:bg-blue-500 px-3 py-1 rounded text-sm transition-colors"
        >
          Logout
        </button>
      </template>
      <template v-else>
        <button
          @click="showSignup = true"
          class="border border-blue-400 hover:bg-blue-700 px-3 py-1 rounded text-sm transition-colors"
        >
          Sign Up
        </button>
        <button
          @click="showLogin = true"
          class="bg-blue-600 hover:bg-blue-500 px-3 py-1 rounded text-sm transition-colors"
        >
          Login
        </button>
      </template>
    </div>

    <LoginModal v-model="showLogin" @success="onLoginSuccess" />
    <SignupModal v-model="showSignup" @success="onLoginSuccess" />
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import LoginModal from './login.vue'
import SignupModal from './signup.vue'

const router = useRouter()
const showLogin = ref(false)
const showSignup = ref(false)
const loggedIn = ref(false)
const username = ref('')

onMounted(() => {
  const token = localStorage.getItem('token')
  const user = JSON.parse(localStorage.getItem('user') || '{}')
  if (token && user.username) {
    loggedIn.value = true
    username.value = user.username
  }
})

function onLoginSuccess(user) {
  loggedIn.value = true
  username.value = user?.username || ''
}

function logout() {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  loggedIn.value = false
  username.value = ''
  router.push('/')
}
</script>
