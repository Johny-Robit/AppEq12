<template>
  <div class="profile-container">
    <h1>Profile</h1>
    <p><strong>Name:</strong> {{ user.username }}</p>
    <p><strong>Email:</strong> {{ user.email }}</p>
    <RouterLink to="/edit-profile" class="button">Edit Profile</RouterLink>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { isLoggedIn, user } from '../auth.js'

const router = useRouter()

onMounted(() => {
  if (!isLoggedIn.value) {
    router.push({ path: '/login', query: { redirect: '/profile' } })
  }
})
</script>

<style scoped>
.profile-container {
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

.button {
  padding: 0.5em 1em;
  border: none;
  border-radius: 4px;
  background-color: #42b983;
  color: white;
  cursor: pointer;
  text-decoration: none;
}

.button:hover {
  background-color: #369f6b;
}
</style>
