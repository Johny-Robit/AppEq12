<template>
  <div>
    <div class="event-container" v-if="event">
      <h1>{{ event.event_name }}</h1>
      <p><strong>Address:</strong> {{ event.event_address }}</p>
      <p><strong>Date & Time:</strong>From {{ formatDateTime(event.start_datetime) }} To {{ formatDateTime(event.end_datetime) }}</p>
      <p><strong>Attendees:</strong> {{ attendees.length + 1 }}</p> <!-- Include creator in the count -->
      <p><strong>Created by:</strong> {{ getUsername(event.ownerID) }}</p>
      <p>{{ event.description }}</p>
      <div v-if="isCreator">
        <button @click="editEvent(event.event_id)">Edit Event</button>
        <button @click="confirmDeleteEvent(event.event_id)">Delete Event</button>
        <button @click="inviteSomeone(event.event_id)">Invite Someone</button>
      </div>
      <div v-else>
        <button @click="handleJoinEvent(event.event_id)" v-if="!isJoined">Join Event</button>
        <button @click="handleLeaveEvent(event.event_id)" v-if="isJoined">Leave Event</button>
        <button @click="inviteSomeone(event.event_id)">Invite Someone</button>
      </div>
    </div>
    <div class="attendees-container" v-if="event">
      <h3>Attendees</h3>
      <div class="attendees-list">
        <div class="attendee-item">
          {{ getUsername(event.ownerID) }} <!-- Directly include creator's username -->
        </div>
        <div v-for="attendee in attendees" :key="attendee.id" class="attendee-item">
          {{ getUsername(attendee.id) }}
          <button v-if="isCreator" @click="removeAttendee(attendee.id)">Remove</button>
        </div>
      </div>
    </div>
    <div class="pending-invites-container" v-if="isCreator && pendingInvites.length">
      <h3>Pending Invites</h3>
      <div class="pending-invites-list">
        <div v-for="invite in pendingInvites" :key="invite.user_id" class="pending-invite-item">
          {{ getUsername(invite.id) }}
        </div>
      </div>
    </div>
    <InvitePopup :visible="isPopupVisible" :users="users" :eventId="Number(eventId)" @close="isPopupVisible = false" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getEventInformation, deleteEvent as deleteEventAPI, getAttendeesList, removeAttendee as removeAttendeeAPI, getPendingInvites } from '../api/event'
import { getAllUsers, getCreatedEventsList, getJoinedEventsList } from '../api/user' // Import getJoinedEventsList
import { isLoggedIn, user } from '../store/user'
import { joinEvent as joinEventAPI, leaveEvent as leaveEventAPI } from '../api/event'
import InvitePopup from '../components/InvitePopup.vue'

const event = ref(null)
const isJoined = ref(false)
const isCreator = ref(false)
const users = ref([]) // Define users
const attendees = ref([]) // Define attendees
const pendingInvites = ref([]) // Define pending invites
const joinedEventIds = ref([]) // Define joinedEventIds
const createdEventIds = ref([]) // Define createdEventIds
const isPopupVisible = ref(false)
const router = useRouter()
const route = useRoute()
const eventId = Number(route.params.id) // Ensure eventId is a number

const fetchEvent = async () => {
  try {
    const response = await getEventInformation(eventId)
    event.value = response
  } catch (error) {
    console.error('Failed to fetch event information:', error)
  }
}

const fetchUsers = async () => {
  try {
    const token = localStorage.getItem('token')
    users.value = await getAllUsers(token)
  } catch (error) {
    console.error('Failed to fetch users:', error)
  }
}

const fetchAttendees = async () => {
  try {
    const token = localStorage.getItem('token')
    attendees.value = await getAttendeesList(token, eventId)
  } catch (error) {
    console.error('Failed to fetch attendees:', error)
  }
}

const fetchPendingInvites = async () => {
  try {
    const token = localStorage.getItem('token')
    pendingInvites.value = await getPendingInvites(token, eventId)
  } catch (error) {
    console.error('Failed to fetch pending invites:', error)
  }
}

const removeAttendee = async (userId) => {
  if (confirm('Are you sure you want to remove this attendee?')) {
    try {
      const token = localStorage.getItem('token')
      await removeAttendeeAPI(token, eventId, userId)
      await fetchAttendees() // Refresh attendees list
    } catch (error) {
      console.error('Failed to remove attendee:', error)
    }
  }
}

onMounted(async () => {
  await fetchEvent()
  await fetchUsers()
  await fetchAttendees()
  // Fetch joined events to initialize joinedEventIds
  try {
    const token = localStorage.getItem('token')
    const joinedEvents = await getJoinedEventsList(token)
    const createdEvents = await getCreatedEventsList(token)
    joinedEventIds.value = joinedEvents.map(event => event.event_id)
    createdEventIds.value = createdEvents.map(event => event.event_id)
    isJoined.value = joinedEventIds.value.includes(parseInt(eventId))
    isCreator.value = createdEventIds.value.includes(parseInt(eventId))
    if (isCreator.value) {
      await fetchPendingInvites()
    }
  } catch (error) {
    console.error('Failed to fetch joined events:', error)
  }
})

const formatDateTime = (dateTime) => {
  return dateTime.replace('T', ' ')
}

const getUsername = (userId) => {
  const user = users.value.find(user => user.user_id === userId)
  return user ? user.username : 'Unknown'
}

const joinEvent = async (eventId) => {
  try {
    const token = localStorage.getItem('token')
    await joinEventAPI(token, eventId)
    joinedEventIds.value.push(eventId)
    isJoined.value = true
    await fetchAttendees() // Refresh attendees list
  } catch (error) {
    console.error('Failed to join event:', error)
  }
}

const leaveEvent = async (eventId) => {
  try {
    const token = localStorage.getItem('token')
    await leaveEventAPI(token, eventId)
    const index = joinedEventIds.value.indexOf(eventId)
    if (index !== -1) {
      joinedEventIds.value.splice(index, 1)
      isJoined.value = false
      await fetchAttendees() // Refresh attendees list
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

const deleteEvent = async (eventId) => {
  try {
    const token = localStorage.getItem('token')
    await deleteEventAPI(token, eventId)
    router.push('/events')
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
  isPopupVisible.value = true
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

.attendees-container,
.pending-invites-container {
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

.attendees-list,
.pending-invites-list {
  margin-top: 2em;
}

.attendee-item,
.pending-invite-item {
  padding: 0.5em 0;
  border-bottom: 1px solid #495057;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
