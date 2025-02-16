<template>
  <nav>
    <div class="left">
      <RouterLink to="/" class="brand">Eventify</RouterLink>
    </div>
    <div class="center">
      <RouterLink to="/events">Events</RouterLink>
    </div>
    <div class="right">
      <RouterLink to="/create-event" class="button">Create an Event</RouterLink>
      <RouterLink to="/my-events">My Events</RouterLink>
      <div class="separator"></div>
      <RouterLink v-if="!isLoggedIn && !isAuthPage" to="/login">Login</RouterLink>
      <div v-if="isLoggedIn" class="avatar-container" @click="toggleDropdown">
        <img src="../assets/Default_Avatar_Icon.jpg" alt="Avatar" class="avatar" />
        <div v-if="dropdownVisible" class="dropdown-menu">
          <RouterLink to="/profile">Profile</RouterLink>
          <button @click="logout">Logout</button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { isLoggedIn } from '../auth.js'

const route = useRoute()
const router = useRouter()
const isAuthPage = route.path === '/login' || route.path === '/signup'
const dropdownVisible = ref(false)

const toggleDropdown = () => {
  dropdownVisible.value = !dropdownVisible.value
}

const logout = () => {
  isLoggedIn.value = false
  router.push('/')
}
</script>

<style scoped>
nav {
  display: flex;
  justify-content: space-between;
  background-color: #343a40;
  color: white;
  padding: 1em;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  width: 100%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

nav a {
  color: white;
  text-decoration: none;
}

nav a:hover {
  text-decoration: underline;
}

.left {
  display: flex;
  align-items: center;
  gap: 1em;
}

.center {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-grow: 1;
}

.right {
  display: flex;
  align-items: center;
  gap: 1em;
  margin-right: 2em;
}

.separator {
  height: 1.5em;
  width: 1px;
  background-color: white;
  margin-right: 1em;
}

.brand {
  font-size: 1.5em;
  font-weight: bold;
  color: #42b983;
}

.button {
  padding: 0.5em 1em;
  border: none;
  border-radius: 4px;
  background-color: #42b983;
  color: white;
  cursor: pointer;
}

.button:hover {
  background-color: #369f6b;
}

.avatar-container {
  position: relative;
  cursor: pointer;
}

.avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
}

.dropdown-menu {
  position: absolute;
  top: 40px;
  right: 0;
  background-color: #343a40;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
}

.dropdown-menu a,
.dropdown-menu button {
  padding: 0.5em 1em;
  color: white;
  text-align: left;
  background: none;
  border: none;
  cursor: pointer;
}

.dropdown-menu a:hover,
.dropdown-menu button:hover {
  background-color: #369f6b;
}
</style>
