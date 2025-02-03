<template>
  <nav>
    <div class="left">
      <RouterLink to="/" class="brand">Eventify</RouterLink>
    </div>
    <div class="right">
      <RouterLink to="/login">Login</RouterLink>
    </div>
  </nav>
</template>

<script setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
nav {
  display: flex;
  justify-content: space-between; /* Space between left and right sections */
  background-color: #343a40; /* Darker grey background */
  color: white; /* White text color */
  padding: 1em;
  position: fixed;
  top: 0;
  left: 0; /* Ensure the bar starts from the left edge */
  right: 0; /* Ensure the bar ends at the right edge */
  width: 100%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

nav a {
  color: white; /* Ensure links are white */
  text-decoration: none;
}

nav a:hover {
  text-decoration: underline;
}

.left {
  display: flex;
  align-items: center;
}

.right {
  display: flex;
  align-items: center;
  gap: 1em;
  margin-right: 2em; /* Add more space to the rightmost side */
}

.brand {
  font-size: 1.5em; /* Smaller version of the home page text */
  font-weight: bold;
  color: #42b983; /* Same color as the home page text */
}
</style>
