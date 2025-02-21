<template>
  <div class="profile-container">
    <h1>Profile</h1>
    <p><strong>Username:</strong> {{ user.username }}</p>
    <p><strong>Description:</strong> {{ user.description }}</p>
    <RouterLink to="/edit-profile" class="button">Edit description</RouterLink>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { isLoggedIn, user, fetchUserProfile } from '../store/user' // Import the user store

const router = useRouter()

onMounted(async () => {
  if (!isLoggedIn.value) {
    router.push({ path: '/login', query: { redirect: '/profile' } })
  } else {
    await fetchUserProfile()
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
