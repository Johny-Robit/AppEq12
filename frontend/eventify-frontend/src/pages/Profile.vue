<template>
  <div class="profile-container">
    <h1>Profile</h1>
    <p><strong>Username:</strong> {{ user.username }}</p>
    <p><strong>Description:</strong> {{ user.description }}</p>
    <div class="toggle-container">
      <label for="profile-toggle">Enable Notifications:</label>
      <input type="checkbox" id="profile-toggle" v-model="isNotificationsEnabled" @change="saveToggleState" />
    </div>
    <RouterLink to="/AppEq12/edit-profile" class="button">Edit description</RouterLink>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { isLoggedIn, user, fetchUserProfile } from '../store/user' // Import the user store

const router = useRouter()
const isNotificationsEnabled = ref(false)

const saveToggleState = () => {
  localStorage.setItem('notificationsEnabled', isNotificationsEnabled.value)
}

onMounted(async () => {
  if (!isLoggedIn.value) {
    router.push({ path: '/AppEq12/login', query: { redirect: '/AppEq12/profile' } })
  } else {
    await fetchUserProfile()
    isNotificationsEnabled.value = localStorage.getItem('notificationsEnabled') === 'true'
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

.toggle-container {
  margin: 1em 0;
  display: flex;
  align-items: center;
  gap: 1em;
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
