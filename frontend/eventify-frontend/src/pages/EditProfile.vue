<template>
  <div class="edit-profile-container">
    <h1>Edit Profile</h1>
    <form @submit.prevent="confirmUpdateProfile">
      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" v-model="username" required />
      </div>
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" v-model="email" required />
      </div>
      <div class="form-group">
        <label for="password">New Password:</label>
        <input type="password" v-model="password" />
      </div>
      <div class="form-group">
        <label for="confirmPassword">Confirm New Password:</label>
        <input type="password" v-model="confirmPassword" />
      </div>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      <button type="submit">Update Profile</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { isLoggedIn, user } from '../auth.js'

const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const errorMessage = ref('')

const router = useRouter()

onMounted(() => {
  if (!isLoggedIn.value) {
    router.push({ path: '/login', query: { redirect: '/edit-profile' } })
  } else {
    username.value = user.value.username
    email.value = user.value.email
  }
})

const updateProfile = () => {
  if (password.value && password.value !== confirmPassword.value) {
    errorMessage.value = 'Passwords do not match'
    return
  }

  user.value.username = username.value
  user.value.email = email.value
  if (password.value) {
    user.value.password = password.value
  }
  console.log('Profile updated:', user.value)
  router.push('/profile')
}

const confirmUpdateProfile = () => {
  if (confirm('Are you sure you want to update your profile?')) {
    updateProfile()
  }
}
</script>

<style scoped>
.edit-profile-container {
  border: 1px solid #ccc;
  padding: 2em;
  border-radius: 8px;
  background-color: #343a40;
  color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  max-width: 600px;
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

.error {
  color: red;
  margin-bottom: 1em;
}
</style>
