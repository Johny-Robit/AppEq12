<template>
  <div class="event-container" v-if="event">
    <h1>{{ event.name }}</h1>
    <p><strong>Address:</strong> {{ event.address }}</p>
    <p><strong>Date & Time:</strong> {{ formatDateTime(event.dateTime) }} - {{ formatDateTime(event.endTime) }}</p>
    <p><strong>Attendees:</strong> {{ event.attendees }}</p>
    <p><strong>Created by:</strong> {{ event.createdBy }}</p>
    <p>{{ event.description }}</p>
    <div v-if="isCreator">
      <button @click="inviteSomeone(event.id)">Invite Someone</button>
      <button @click="editEvent(event.id)">Edit Event</button>
      <button @click="confirmDeleteEvent(event.id)">Delete Event</button>
    </div>
    <div v-else>
      <button @click="handleJoinEvent(event.id)" v-if="!isJoined">Join Event</button>
      <button @click="handleLeaveEvent(event.id)" v-if="isJoined">Leave Event</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { events, joinedEventIds } from '../events.js'
import { isLoggedIn, user } from '../store/user.js'
import { joinEvent as joinEventAPI, leaveEvent as leaveEventAPI } from '../api/event'

const event = ref(null)
const isJoined = ref(false)
const isCreator = ref(false)
const router = useRouter()
const route = useRoute()
const eventId = route.params.id

onMounted(() => {
  event.value = events.value.find(e => e.id === parseInt(eventId))
  isJoined.value = joinedEventIds.value.includes(parseInt(eventId))
  isCreator.value = event.value && event.value.createdBy === user.value.username
})

const formatDateTime = (dateTime) => {
  return dateTime.replace('T', ' ')
}

const joinEvent = async (eventId) => {
  const token = user.value.token
  try {
    await joinEventAPI(token, eventId)
    joinedEventIds.value.push(eventId)
    isJoined.value = true
    console.log(`Joined event with ID: ${eventId}`)
  } catch (error) {
    console.error('Failed to join event:', error)
  }
}

const leaveEvent = async (eventId) => {
  const token = user.value.token
  try {
    await leaveEventAPI(token, eventId)
    const index = joinedEventIds.value.indexOf(eventId)
    if (index !== -1) {
      joinedEventIds.value.splice(index, 1)
      isJoined.value = false
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
    joinEvent(eventId)
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

const deleteEvent = (eventId) => {
  const index = events.value.findIndex(event => event.id === eventId)
  if (index !== -1) {
    events.value.splice(index, 1)
    console.log(`Deleted event with ID: ${eventId}`)
    router.push('/events')
  }
}

const confirmDeleteEvent = (eventId) => {
  if (confirm('Are you sure you want to delete this event?')) {
    deleteEvent(eventId)
  }
}

const inviteSomeone = (eventId) => {
  console.log(`Inviting someone to event with ID: ${eventId}`)
  // Add logic to invite someone to the event
}
</script>

<style scoped>
.event-container {
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

button {
  padding: 0.5em 1em;
  border: none;
  border-radius: 4px;
  background-color: #42b983;
  color: white;
  cursor: pointer;
  margin-right: 0.5em;
}

button:hover {
  background-color: #369f6b;
}
</style>
