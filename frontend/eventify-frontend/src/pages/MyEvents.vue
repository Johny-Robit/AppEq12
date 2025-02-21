<template>
  <div class="container">
    <h1>My Events</h1>
    <div class="tabs">
      <button :class="{ active: activeTab === 'joined' }" @click="activeTab = 'joined'">Joined Events</button>
      <button :class="{ active: activeTab === 'created' }" @click="activeTab = 'created'">Created Events</button>
      <button :class="{ active: activeTab === 'invitations' }" @click="activeTab = 'invitations'">Event Invitations</button>
      <button :class="{ active: activeTab === 'past' }" @click="activeTab = 'past'">Past Events</button>
    </div>
    <div class="events-container">
      <div v-if="activeTab === 'joined'" class="joined-events">
        <div v-if="joinedEvents.length">
          <div v-for="event in joinedEvents" :key="event.event_id" class="event">
            <h3 @click="goToEvent(event.event_id)" class="event-name">{{ event.event_name }}</h3>
            <p><strong>Address:</strong> {{ event.event_address }}</p>
            <p><strong>Date & Time:</strong> {{ formatDateTime(event.start_datetime) }} - {{ formatDateTime(event.end_datetime) }}</p>
            <p><strong>Attendees:</strong> {{ event.attendees }}</p>
            <p><strong>Created by:</strong> {{ getUsername(event.ownerID) }}</p>
            <p>{{ event.description }}</p>
            <button @click="confirmLeaveEvent(event.event_id)">Leave Event</button>
            <button @click="inviteSomeone(event.event_id)">Invite Someone</button>
          </div>
        </div>
        <p v-else>You have not joined any events yet.</p>
      </div>
      <div v-if="activeTab === 'created'" class="created-events">
        <div v-if="createdEvents.length">
          <div v-for="event in createdEvents" :key="event.event_id" class="event">
            <h3 @click="goToEvent(event.event_id)" class="event-name">{{ event.event_name }}</h3>
            <p><strong>Address:</strong> {{ event.event_address }}</p>
            <p><strong>Date & Time:</strong> {{ formatDateTime(event.start_datetime) }} - {{ formatDateTime(event.end_datetime) }}</p>
            <p><strong>Attendees:</strong> {{ event.attendees }}</p>
            <p><strong>Created by:</strong> {{ getUsername(event.ownerID) }}</p>
            <p>{{ event.description }}</p>
            <button @click="editEvent(event.event_id)">Edit</button>
            <button @click="confirmDeleteEvent(event.event_id)">Delete</button>
            <button @click="inviteSomeone(event.event_id)">Invite Someone</button>
          </div>
        </div>
        <p v-else>You have not created any events yet.</p>
        <button @click="goToCreateEvent" class="create-event-button">Create an Event</button>
      </div>
      <div v-if="activeTab === 'invitations'" class="event-invitations">
        <div v-if="eventInvitationsList.length">
          <div v-for="event in eventInvitationsList" :key="event.event_id" class="event">
            <h3 @click="goToEvent(event.event_id)" class="event-name">{{ event.event_name }}</h3>
            <p><strong>Address:</strong> {{ event.event_address }}</p>
            <p><strong>Date & Time:</strong> {{ formatDateTime(event.start_datetime) }} - {{ formatDateTime(event.end_datetime) }}</p>
            <p><strong>Attendees:</strong> {{ event.attendees }}</p>
            <p><strong>Created by:</strong> {{ getUsername(event.ownerID) }}</p>
            <p>{{ event.description }}</p>
            <button @click="confirmJoinEvent(event.event_id)">Join Event</button>
          </div>
        </div>
        <p v-else>You have no event invitations.</p>
      </div>
      <div v-if="activeTab === 'past'" class="past-events">
        <div v-if="pastEvents.length">
          <div v-for="event in pastEvents" :key="event.event_id" class="event">
            <h3 @click="goToEvent(event.event_id)" class="event-name">{{ event.event_name }}</h3>
            <p><strong>Address:</strong> {{ event.event_address }}</p>
            <p><strong>Date & Time:</strong> {{ formatDateTime(event.start_datetime) }} - {{ formatDateTime(event.end_datetime) }}</p>
            <p><strong>Attendees:</strong> {{ event.attendees }}</p>
            <p><strong>Created by:</strong> {{ getUsername(event.ownerID) }}</p>
            <p>{{ event.description }}</p>
          </div>
        </div>
        <p v-else>You have no past events.</p>
      </div>
    </div>
    <InvitePopup :visible="isPopupVisible" :users="users" :eventId="selectedEventId" @close="isPopupVisible = false" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { isLoggedIn, user } from '../store/user'
import { getJoinedEventsList, getCreatedEventsList, getEventInvitesList, getAllUsers } from '../api/user'
import { joinEvent as joinEventAPI, leaveEvent as leaveEventAPI, deleteEvent as deleteEventAPI } from '../api/event'
import InvitePopup from '../components/InvitePopup.vue'

const router = useRouter()
const route = useRoute()

const activeTab = ref('joined') // Set default active tab to 'joined'
const joinedEvents = ref([])
const createdEvents = ref([])
const eventInvitationsList = ref([])
const users = ref([]) // Define users
const pastEvents = computed(() => {
  return [...joinedEvents.value, ...createdEvents.value].filter(event => new Date(event.end_datetime) < new Date())
})

const isPopupVisible = ref(false)
const selectedEventId = ref(null)

onMounted(async () => {
  if (!isLoggedIn.value) {
    router.push({ path: '/login', query: { redirect: route.fullPath } })
  } else {
    try {
      const token = localStorage.getItem('token')
      joinedEvents.value = await getJoinedEventsList(token)
      createdEvents.value = await getCreatedEventsList(token)
      eventInvitationsList.value = await getEventInvitesList(token)
      users.value = await getAllUsers(token)
    } catch (error) {
      console.error('Failed to fetch events:', error)
    }
  }
})

const getUsername = (userId) => {
  const user = users.value.find(user => user.user_id === userId)
  return user ? user.username : 'Unknown'
}

const joinEvent = async (eventId) => {
  try {
    const token = localStorage.getItem('token')
    await joinEventAPI(token, eventId)
    joinedEvents.value = await getJoinedEventsList(token)
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
    joinedEvents.value = await getJoinedEventsList(token)
  } catch (error) {
    console.error('Failed to leave event:', error)
  }
}

const confirmLeaveEvent = (eventId) => {
  if (confirm('Are you sure you want to leave this event?')) {
    leaveEvent(eventId)
  }
}

const deleteEvent = async (eventId) => {
  try {
    const token = localStorage.getItem('token')
    await deleteEventAPI(token, eventId)
    createdEvents.value = await getCreatedEventsList(token)
  } catch (error) {
    console.error('Failed to delete event:', error)
  }
}

const confirmDeleteEvent = (eventId) => {
  if (confirm('Are you sure you want to delete this event?')) {
    deleteEvent(eventId)
  }
}

const editEvent = (eventId) => {
  router.push({ path: `/edit-event/${eventId}` })
}

const inviteSomeone = (eventId) => {
  selectedEventId.value = eventId
  isPopupVisible.value = true
}

const formatDateTime = (dateTime) => {
  if (!dateTime) return 'N/A';
  return dateTime.replace('T', ' ')
}

const goToEvent = (eventId) => {
  router.push({ path: `/event/${eventId}` })
}

const goToCreateEvent = () => {
  router.push({ path: '/create-event' })
}
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.tabs {
  display: flex;
  gap: 0.2em;
  margin-bottom: 1em;
}

.tabs button {
  padding: 0.5em 1em;
  border: none;
  border-radius: 4px;
  background-color: #42b983;
  color: white;
  cursor: pointer;
}

.tabs button.active {
  background-color: #24704a;
}

.events-container {
  width: 100%;
}

h1 {
  color: #42b983;
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

.event-name {
  cursor: pointer;
  color: #42b983;
}

event-name:hover {
  text-decoration: underline;
}

.create-event-button {
  background-color: #42b983;
  color: white;
  border: none;
  padding: 0.5em 1em;
  cursor: pointer;
  margin-top: 1em;
}

.create-event-button:hover {
  background-color: #369f6b;
}
</style>
