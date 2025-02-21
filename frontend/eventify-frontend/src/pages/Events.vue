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
    <div v-for="event in filteredEvents" :key="event.event_id" class="event">
      <h2 @click="goToEvent(event.event_id)" class="event-name">{{ event.event_name }}</h2>
      <p><strong>Address:</strong> {{ event.event_address }}</p>
      <p><strong>Date & Time:</strong> From {{ event.start_datetime }} To {{ event.end_datetime }}</p>
      <p><strong>Attendees:</strong> 53 </p>
      <p><strong>Created by:</strong> {{ getUsername(event.ownerID) }}</p>
      <p>{{ event.description }}</p>
      <div class="button-group">
        <div v-if="!isCreator(event.event_id)">
          <button v-if="!isJoined(event.event_id)" @click="handleJoinEvent(event.event_id)">Join Event</button>
          <button v-else @click="handleLeaveEvent(event.event_id)">Leave Event</button>
        </div>
        <div v-if="isCreator(event.event_id)">
          <button @click="editEvent(event.event_id)">Edit</button>
          <button class="delete-button" @click="confirmDeleteEvent(event.event_id)">Delete</button>
        </div>
        <button @click="handleInviteSomeone(event.event_id)">Invite Someone</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getAllEvents } from '../api/event'
import { getAllUsers, getJoinedEventsList, getCreatedEventsList } from '../api/user' // Import getCreatedEventsList
import { isLoggedIn, user } from '../store/user'
import { joinEvent as joinEventAPI, leaveEvent as leaveEventAPI, deleteEvent as deleteEventAPI } from '../api/event'

const searchQuery = ref('')
const searchTrigger = ref('')
const events = ref([])
const joinedEventIds = ref([]) // Define joinedEventIds
const createdEventIds = ref([]) // Define createdEventIds
const users = ref([]) // Define users

const router = useRouter()
const route = useRoute()

const fetchEvents = async () => {
  try {
    const response = await getAllEvents()
    events.value = response
  } catch (error) {
    console.error('Failed to fetch events:', error)
  }
}

const fetchUsers = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await getAllUsers(token)
    users.value = response
  } catch (error) {
    console.error('Failed to fetch users:', error)
  }
}

const fetchJoinedEvents = async () => {
  try {
    const token = localStorage.getItem('token')
    const joinedEvents = await getJoinedEventsList(token)
    joinedEventIds.value = joinedEvents.map(event => event.event_id)
  } catch (error) {
    console.error('Failed to fetch joined events:', error)
  }
}

const fetchCreatedEvents = async () => {
  try {
    const token = localStorage.getItem('token')
    const createdEvents = await getCreatedEventsList(token)
    createdEventIds.value = createdEvents.map(event => event.event_id)
  } catch (error) {
    console.error('Failed to fetch created events:', error)
  }
}

onMounted(async () => {
  await fetchUsers()
  await fetchEvents()
  await fetchJoinedEvents()
  await fetchCreatedEvents()
})

const filteredEvents = computed(() => {
  return events.value.filter(event => 
    event.event_name.toLowerCase().includes(searchTrigger.value.toLowerCase())
  )
})

const getUsername = (userId) => {
  const user = users.value.find(user => user.user_id === userId)
  return user ? user.username : 'Unknown'
}

const performSearch = () => {
  searchTrigger.value = searchQuery.value
}

const clearSearch = () => {
  searchQuery.value = ''
  searchTrigger.value = ''
}

const joinEvent = async (eventId) => {
  try {
    const token = localStorage.getItem('token')
    await joinEventAPI(token, eventId)
    joinedEventIds.value.push(eventId)
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
  try {
    const token = localStorage.getItem('token')
    await leaveEventAPI(token, eventId)
    const index = joinedEventIds.value.indexOf(eventId)
    if (index !== -1) {
      joinedEventIds.value.splice(index, 1)
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

const editEvent = (eventId) => {
  router.push({ path: `/edit-event/${eventId}` })
}

const deleteEvent = async (eventId) => {
  try {
    const token = localStorage.getItem('token')
    await deleteEventAPI(token, eventId)
    const index = events.value.findIndex(event => event.event_id === eventId)
    if (index !== -1) {
      events.value.splice(index, 1)
    }
  } catch (error) {
    console.error('Failed to delete event:', error)
  }
}

const confirmDeleteEvent = (eventId) => {
  if (confirm('Are you sure you want to delete this event?')) {
    deleteEvent(eventId)
  }
}

const inviteSomeone = (eventId) => {
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

const isCreator = (eventId) => {
  return createdEventIds.value.includes(eventId)
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

.button-group {
  display: flex;
  justify-content: center;
  gap: 0.5em;
}

button {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 0.5em 1em;
  cursor: pointer;
}

button:hover {
  background-color: #369f6b;
}

.delete-button {
  margin-left: 0.5em;
}

.event-name {
  cursor: pointer;
  color: #42b983;
}

.event-name:hover {
  text-decoration: underline;
}
</style>
