<template>
  <div class="login-container">
    <h1>Login</h1>
    <form @submit.prevent="login">
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" v-model="email" required />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" v-model="password" required />
      </div>
      <button type="submit">Login</button>
    </form>
    <p>Don't have an account? <RouterLink to="/signup">Sign up here</RouterLink></p>
    <form @submit.prevent="temporaryLogin" v-if="!isLoggedIn">
      <button type="submit">Temporary Login</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter, useRoute } from 'vue-router'
import { isLoggedIn, user } from '../auth.js'

const email = ref('')
const password = ref('')

const router = useRouter()
const route = useRoute()

const login = () => {
  if (email.value === user.value.email && password.value === user.value.password) {
    console.log('Logging in with', email.value, password.value)
    isLoggedIn.value = true
    const redirectTo = route.query.redirect || '/'
    router.push(redirectTo)
  } else {
    console.log('Invalid email or password')
  }
}

const temporaryLogin = () => {
  isLoggedIn.value = true
  console.log('Logged in:', isLoggedIn.value)
  const redirectTo = route.query.redirect || '/'
  router.push(redirectTo)
}
</script>

<style scoped>
.login-container {
  border: 1px solid #ccc;
  padding: 2em;
  border-radius: 8px;
  background-color: #343a40;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  width: 100%;
  margin: 2em auto;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 1em;
}

label {
  margin-bottom: 0.5em;
}

input {
  padding: 0.5em;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 0.5em 1em;
  border: none;
  border-radius: 4px;
  background-color: #42b983;
  color: white;
  cursor: pointer;
}

button:hover {
  background-color: #369f6b;
}
</style>
