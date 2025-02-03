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
  padding-top: 4em;
  display: flex;
  /*justify-content: center;
  align-items: center;*/
  flex-direction: column;
  min-height: 100vh;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
}
</style>
