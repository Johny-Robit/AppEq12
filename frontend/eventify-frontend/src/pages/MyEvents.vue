<template>
  <div class="container">
    <h1>My Events</h1>
    <div class="tabs">
      <button :class="{ active: activeTab === 'joined' }" @click="activeTab = 'joined'">Joined Events</button>
      <button :class="{ active: activeTab === 'invitations' }" @click="activeTab = 'invitations'">Event Invitations</button>
      <button :class="{ active: activeTab === 'created' }" @click="activeTab = 'created'">Created Events</button>
    </div>
    <div class="events-container">
      <div v-if="activeTab === 'joined'" class="joined-events">
        <div v-if="joinedEvents.length">
          <div v-for="event in joinedEvents" :key="event.id" class="event">
            <h3>{{ event.name }}</h3>
            <p><strong>Address:</strong> {{ event.address }}</p>
            <p><strong>Date & Time:</strong> {{ formatDateTime(event.dateTime) }} - {{ formatDateTime(event.endTime) }}</p>
            <p><strong>Attendees:</strong> {{ event.attendees }}</p>
            <p><strong>Created by:</strong> {{ event.createdBy }}</p>
            <p>{{ event.description }}</p>
            <button @click="confirmLeaveEvent(event.id)">Leave Event</button>
          </div>
        </div>
        <p v-else>You have not joined any events yet.</p>
      </div>
      <div v-if="activeTab === 'invitations'" class="event-invitations">
        <div v-if="eventInvitationsList.length">
          <div v-for="event in eventInvitationsList" :key="event.id" class="event">
            <h3>{{ event.name }}</h3>
            <p><strong>Address:</strong> {{ event.address }}</p>
            <p><strong>Date & Time:</strong> {{ formatDateTime(event.dateTime) }} - {{ formatDateTime(event.endTime) }}</p>
            <p><strong>Attendees:</strong> {{ event.attendees }}</p>
            <p><strong>Created by:</strong> {{ event.createdBy }}</p>
            <p>{{ event.description }}</p>
            <button @click="confirmJoinEvent(event.id)">Join Event</button>
          </div>
        </div>
        <p v-else>You have no event invitations.</p>
      </div>
      <div v-if="activeTab === 'created'" class="created-events">
        <div v-if="createdEvents.length">
          <div v-for="event in createdEvents" :key="event.id" class="event">
            <h3>{{ event.name }}</h3>
            <p><strong>Address:</strong> {{ event.address }}</p>
            <p><strong>Date & Time:</strong> {{ formatDateTime(event.dateTime) }} - {{ formatDateTime(event.endTime) }}</p>
            <p><strong>Attendees:</strong> {{ event.attendees }}</p>
            <p><strong>Created by:</strong> {{ event.createdBy }}</p>
            <p>{{ event.description }}</p>
            <button @click="editEvent(event.id)">Edit</button>
            <button @click="confirmDeleteEvent(event.id)">Delete</button>
          </div>
        </div>
        <p v-else>You have not created any events yet.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { isLoggedIn, user } from '../auth.js'
import { joinedEventIds, events, eventInvitations } from '../events.js'

const router = useRouter()
const route = useRoute()

const activeTab = ref('joined')

onMounted(() => {
  if (!isLoggedIn.value) {
    router.push({ path: '/login', query: { redirect: route.fullPath } })
  }
})

const joinedEvents = computed(() => {
  return events.value.filter(event => joinedEventIds.value.includes(event.id))
})

const createdEvents = computed(() => {
  return events.value.filter(event => event.createdBy === user.value.name)
})

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

const leaveEvent = (eventId) => {
  const index = joinedEventIds.value.indexOf(eventId)
  if (index !== -1) {
    joinedEventIds.value.splice(index, 1)
    console.log(`Left event with ID: ${eventId}`)
  }
}

const confirmLeaveEvent = (eventId) => {
  if (confirm('Are you sure you want to leave this event?')) {
    leaveEvent(eventId)
  }
}

const deleteEvent = (eventId) => {
  const index = events.value.findIndex(event => event.id === eventId)
  if (index !== -1) {
    events.value.splice(index, 1)
    console.log(`Deleted event with ID: ${eventId}`)
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

const eventInvitationsList = computed(() => {
  return events.value.filter(event => eventInvitations.value.includes(event.id))
})

const formatDateTime = (dateTime) => {
  return dateTime.replace('T', ' ')
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
</style>
