<script setup>
import NavBar from './components/NavBar.vue'
import { RouterView } from 'vue-router'
</script>

<template>
  <div>
    <NavBar />
    <main>
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
main {
  padding-top: 4em; /* Adjust this value based on the height of your nav bar */
  display: flex;
  justify-content: center; /* Center the main content */
  align-items: center;
  flex-direction: column;
  min-height: 100vh; /* Ensure the main content takes up the full height of the viewport */
  max-width: 1200px; /* Set a maximum width for the main content */
  width: 100%; /* Ensure the main content takes up the full width */
  margin: 0 auto; /* Center the main content horizontally */
}
</style>
