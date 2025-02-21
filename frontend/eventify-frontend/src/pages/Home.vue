<template>
  <div>
    <h1>Welcome to Eventify</h1>
    <p>This is the home page.</p>
    <p v-if="isLoggedIn">You are logged in!</p>
  </div>
</template>

<script setup>
import { isLoggedIn } from '../store/user'

</script>

<style scoped>
h1 {
  color: #42b983;
}
</style>
