<template>
  <div>
    <h1>Events</h1>
    <input v-model="searchQuery" @keyup.enter="performSearch" placeholder="Search events..." />
    <p>Here are some upcoming events.</p>
    <div v-for="event in filteredEvents" :key="event.id" class="event">
      <h2>{{ event.name }}</h2>
      <p><strong>Address:</strong> {{ event.address }}</p>
      <p><strong>Date & Time:</strong> {{ event.dateTime }} - {{ event.endTime }}</p>
      <p><strong>Attendees:</strong> {{ event.attendees }}</p>
      <p><strong>Created by:</strong> {{ event.createdBy }}</p>
      <p>{{ event.description }}</p>
      <button @click="handleJoinEvent(event.id)">Join Event</button>
      <button @click="handleInviteSomeone(event.id)">Invite Someone</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { events, joinedEventIds } from '../events.js'
import { isLoggedIn, user } from '../auth.js'

const searchQuery = ref('')
const searchTrigger = ref('')

const router = useRouter()
const route = useRoute()

const filteredEvents = computed(() => {
  return events.value.filter(event => event.name.toLowerCase().includes(searchTrigger.value.toLowerCase()))
})

const performSearch = () => {
  searchTrigger.value = searchQuery.value
}

const joinEvent = (eventId) => {
  if (!joinedEventIds.value.includes(eventId)) {
    joinedEventIds.value.push(eventId)
  }
  console.log(`Joining event with ID: ${eventId}`)
}

const confirmJoinEvent = (eventId) => {
  if (confirm('Are you sure you want to join this event?')) {
    joinEvent(eventId)
  }
}

const handleJoinEvent = (eventId) => {
  if (!isLoggedIn.value) {
    router.push({ path: '/login', query: { redirect: route.fullPath } })
  } else {
    confirmJoinEvent(eventId)
  }
}

const inviteSomeone = (eventId) => {
  console.log(`Inviting someone to event with ID: ${eventId}`)
  // Add logic to invite someone to the event
}

const handleInviteSomeone = (eventId) => {
  if (!isLoggedIn.value) {
    router.push({ path: '/login', query: { redirect: route.fullPath } })
  } else {
    inviteSomeone(eventId)
  }
}
</script>

<style scoped>
h1 {
  color: #42b983;
}

input {
  margin-bottom: 1em;
  padding: 0.5em;
  width: 100%;
  box-sizing: border-box;
}

.event {
  border: 1px solid #ddd;
  padding: 1em;
  margin-bottom: 1em;
}

button {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 0.5em 1em;
  cursor: pointer;
  margin-right: 0.5em;
}

button:hover {
  background-color: #369f6b;
}
</style>
