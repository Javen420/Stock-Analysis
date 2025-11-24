<template>
  <div v-if="visible" class="modal-backdrop" @keydown.esc="close" tabindex="0">
    <div class="modal" @click.stop>
      <button class="close" @click="close">×</button>
      <h3>Login</h3>

      <div class="form-group">
        <label>Username</label>
        <input v-model="username" type="text" />
      </div>

      <div class="form-group">
        <label>Password</label>
        <input v-model="password" type="password" />
      </div>

      <div class="actions">
        <button @click="submit" :disabled="loading">
          {{ loading ? 'Logging in…' : 'Login' }}
        </button>
      </div>

      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'

const props = defineProps({
  modelValue: { type: Boolean, default: false } // v-model:visible
})
const emit = defineEmits(['update:modelValue', 'success'])

const visible = ref(props.modelValue)
watch(() => props.modelValue, v => (visible.value = v))

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref(null)

onMounted(() => {
  if (visible.value) document.querySelector('.modal')?.focus()
})

function close() {
  emit('update:modelValue', false)
  error.value = null
  username.value = ''
  password.value = ''
}

async function submit() {
  error.value = null
  loading.value = true
  try {
    const res = await fetch('http://localhost:5000/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: username.value, password: password.value })
    })
    const data = await res.json()
    if (!res.ok) {
      error.value = data.error || 'Login failed'
      loading.value = false
      return
    }
    localStorage.setItem('token', data.token)
    localStorage.setItem('user', JSON.stringify(data.user || {}))
    emit('success', data.user || null)
    emit('update:modelValue', false)
  } catch (e) {
    error.value = 'Network error'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.modal-backdrop { position: fixed; inset: 0; background: rgba(0,0,0,0.4); display:flex; align-items:center; justify-content:center; z-index:1000; }
.modal { background:white; padding:1.25rem; border-radius:8px; width:320px; box-shadow:0 10px 30px rgba(0,0,0,0.2); position:relative; }
.close { position:absolute; right:8px; top:8px; border:none; background:transparent; font-size:1.25rem; cursor:pointer; }
.form-group { margin-bottom:0.75rem; }
input { width:100%; padding:0.5rem; border:1px solid #ccc; border-radius:4px; }
.actions { display:flex; justify-content:flex-end; margin-top:0.5rem; }
button[disabled] { opacity:0.6; cursor:not-allowed; }
.error { color:#b91c1c; margin-top:0.5rem; }
</style>