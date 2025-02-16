<template>
  <div class="signup-container">
    <h1>Signup</h1>
    <form @submit.prevent="signup">
      <div class="form-group">
        <label for="name">Username:</label>
        <input type="text" v-model="name" required />
      </div>
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" v-model="email" required />
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" v-model="password" required />
      </div>
      <div class="form-group">
        <label for="confirmPassword">Confirm Password:</label>
        <input type="password" v-model="confirmPassword" required />
      </div>
      <button type="submit">Signup</button>
    </form>
    <p>Already have an account? <RouterLink to="/login">Login here</RouterLink></p>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const name = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')

const signup = () => {
  if (password.value !== confirmPassword.value) {
    alert('Passwords do not match')
    return
  }
  console.log('Signing up with', name.value, email.value, password.value)
}
</script>

<style scoped>
.signup-container {
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

.back-to-login {
  display: block;
  margin-top: 1em;
  color: #42b983;
  text-align: center;
}

.back-to-login:hover {
  text-decoration: underline;
}
</style>
