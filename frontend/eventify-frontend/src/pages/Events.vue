<template>
  <div>
    <h1>Events</h1>
    <div class="search-container">
      <input v-model="searchQuery" @keyup.enter="performSearch" placeholder="Search events..." />
      <button v-if="searchQuery" @click="clearSearch" class="clear-button">X</button>
      <button @click="performSearch" class="button">
        Search
      </button>
    </div>
    <p>Here are some upcoming events.</p>
    <div v-for="event in filteredEvents" :key="event.id" class="event">
      <h2 @click="goToEvent(event.id)" class="event-name">{{ event.name }}</h2>
      <p><strong>Address:</strong> {{ event.address }}</p>
      <p><strong>Date & Time:</strong> From {{ event.dateTime }} To {{ event.endTime }}</p>
      <p><strong>Attendees:</strong> {{ event.attendees }}</p>
      <p><strong>Created by:</strong> {{ event.createdBy }}</p>
      <p>{{ event.description }}</p>
      <button v-if="!isJoined(event.id)" @click="handleJoinEvent(event.id)">Join Event</button>
      <button v-else @click="handleLeaveEvent(event.id)">Leave Event</button>
      <button @click="handleInviteSomeone(event.id)">Invite Someone</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { events, joinedEventIds } from '../events.js'
import { isLoggedIn, user } from '../store/user'
import { joinEvent as joinEventAPI, leaveEvent as leaveEventAPI } from '../api/event'

const searchQuery = ref('')
const searchTrigger = ref('')

const router = useRouter()
const route = useRoute()

const filteredEvents = computed(() => {
  return events.value.filter(event => 
    !event.isPrivate && event.name.toLowerCase().includes(searchTrigger.value.toLowerCase())
  )
})

const performSearch = () => {
  searchTrigger.value = searchQuery.value
}

const clearSearch = () => {
  searchQuery.value = ''
  searchTrigger.value = ''
}

const joinEvent = async (eventId) => {
  const token = user.value.token
  try {
    await joinEventAPI(token, eventId)
    joinedEventIds.value.push(eventId)
    console.log(`Joined event with ID: ${eventId}`)
  } catch (error) {
    console.error('Failed to join event:', error)
  }
}

const confirmJoinEvent = (eventId) => {
  if (confirm('Are you sure you want to join this event?')) {
    joinEvent(eventId)
  }
}

const leaveEvent = async (eventId) => {
  const token = user.value.token
  try {
    await leaveEventAPI(token, eventId)
    const index = joinedEventIds.value.indexOf(eventId)
    if (index !== -1) {
      joinedEventIds.value.splice(index, 1)
      console.log(`Left event with ID: ${eventId}`)
    }
  } catch (error) {
    console.error('Failed to leave event:', error)
  }
}

const handleJoinEvent = (eventId) => {
  if (!isLoggedIn.value) {
    router.push({ path: '/login', query: { redirect: route.fullPath } })
  } else {
    confirmJoinEvent(eventId)
  }
}

const handleLeaveEvent = (eventId) => {
  if (confirm('Are you sure you want to leave this event?')) {
    leaveEvent(eventId)
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

const goToEvent = (eventId) => {
  router.push({ path: `/event/${eventId}` })
}

const isJoined = (eventId) => {
  return joinedEventIds.value.includes(eventId)
}
</script>

<style scoped>
h1 {
  color: #42b983;
}

.search-container {
  display: flex;
  align-items: center;
  margin-bottom: 1em;
}

.clear-button {
  background: none;
  border: none;
  cursor: pointer;
  margin-left: 0.5em;
  color: #646464;
}

input {
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
  margin-left: 0.5em;
}

button:hover {
  background-color: #369f6b;
}

.event-name {
  cursor: pointer;
  color: #42b983;
}

.event-name:hover {
  text-decoration: underline;
}
</style>
