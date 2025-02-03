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
      <button v-if="isLoggedIn" @click="logout">Logout</button>
    </div>
  </nav>
</template>

<script setup>
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { isLoggedIn } from '../auth.js'

const route = useRoute()
const router = useRouter()
const isAuthPage = route.path === '/login' || route.path === '/signup'

console.log('NavBar isLoggedIn:', isLoggedIn.value)

const logout = () => {
  isLoggedIn.value = false
  console.log('Logged out:', isLoggedIn.value)
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

button {
  background: none;
  border: none;
  color: white;
  cursor: pointer;
  font-size: 1em;
}

button:hover {
  text-decoration: underline;
}
</style>
