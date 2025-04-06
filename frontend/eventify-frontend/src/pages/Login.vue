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
    <p>Don't have an account? <RouterLink to="/AppEq12/signup">Sign up here</RouterLink></p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter, useRoute } from 'vue-router'
import { login as loginAPI } from '../api/user' // Import the login API function
import { isLoggedIn, fetchUserProfile } from '../store/user' // Import isLoggedIn and fetchUserProfile from the user store

const email = ref('')
const password = ref('')

const router = useRouter()
const route = useRoute()

const login = async () => {
  try {
    const credentials = {
      email: email.value,
      password: password.value
    }
    const response = await loginAPI(credentials)
    // The loginAPI function now automatically sets the token within a cookie
    if (response){
      isLoggedIn.value = true
      await fetchUserProfile()
    } else {
      isLoggedIn.value = false
      throw new Error (response.error)
    }
    
    const redirectTo = route.query.redirect || '/AppEq12'
    router.push(redirectTo)
  } catch (error) {
    console.error('Login error:', error)
    alert('Login failed: ' + error.error)
  }
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
