<template>
  <div class="container">
    <h1>My Events</h1>
    <div class="tabs">
      <!-- <button :class="{ active: activeTab === 'joined' }" @click="activeTab = 'joined'">Joined Events</button> -->
      <!-- <button :class="{ active: activeTab === 'invitations' }" @click="activeTab = 'invitations'">Event Invitations</button> -->
      <button :class="{ active: activeTab === 'created' }" @click="activeTab = 'created'">Created Events</button>
      <!-- <button :class="{ active: activeTab === 'past' }" @click="activeTab = 'past'">Past Events</button> -->
    </div>
    <div class="events-container">
      <!-- <div v-if="activeTab === 'joined'" class="joined-events">
        <div v-if="joinedEvents.length">
          <div v-for="event in joinedEvents" :key="event.id" class="event">
            <h3 @click="goToEvent(event.id)" class="event-name">{{ event.name }}</h3>
            <p><strong>Address:</strong> {{ event.address }}</p>
            <p><strong>Date & Time:</strong> {{ formatDateTime(event.dateTime) }} - {{ formatDateTime(event.endTime) }}</p>
            <p><strong>Attendees:</strong> {{ event.attendees }}</p>
            <p><strong>Created by:</strong> {{ event.createdBy }}</p>
            <p>{{ event.description }}</p>
            <button @click="confirmLeaveEvent(event.id)">Leave Event</button>
          </div>
        </div>
        <p v-else>You have not joined any events yet.</p>
      </div> -->
      <div v-if="activeTab === 'created'" class="created-events">
        <div v-if="createdEvents.length">
          <div v-for="event in createdEvents" :key="event.id" class="event">
            <h3 @click="goToEvent(event.id)" class="event-name">{{ event.event_name }}</h3>
            <p><strong>Address:</strong> {{ event.event_address }}</p>
            <p><strong>Date & Time:</strong> {{ formatDateTime(event.start_datetime) }} - {{ formatDateTime(event.end_datetime) }}</p>
            <p><strong>Attendees:</strong> {{ event.attendees }}</p>
            <p><strong>Created by:</strong> {{ event.Owner_id }}</p>
            <p>{{ event.description }}</p>
            <button @click="inviteSomeone(event.id)">Invite Someone</button>
            <button @click="editEvent(event.id)">Edit</button>
            <button @click="confirmDeleteEvent(event.id)">Delete</button>
          </div>
        </div>
        <p v-else>You have not created any events yet.</p>
        <button @click="goToCreateEvent" class="create-event-button">Create an Event</button>
      </div>
      <!-- <div v-if="activeTab === 'invitations'" class="event-invitations">
        <div v-if="eventInvitationsList.length">
          <div v-for="event in eventInvitationsList" :key="event.id" class="event">
            <h3 @click="goToEvent(event.id)" class="event-name">{{ event.name }}</h3>
            <p><strong>Address:</strong> {{ event.address }}</p>
            <p><strong>Date & Time:</strong> {{ formatDateTime(event.dateTime) }} - {{ formatDateTime(event.endTime) }}</p>
            <p><strong>Attendees:</strong> {{ event.attendees }}</p>
            <p><strong>Created by:</strong> {{ event.createdBy }}</p>
            <p>{{ event.description }}</p>
            <button @click="confirmJoinEvent(event.id)">Join Event</button>
          </div>
        </div>
        <p v-else>You have no event invitations.</p>
      </div> -->
      <!-- <div v-if="activeTab === 'past'" class="past-events">
        <div v-if="pastEvents.length">
          <div v-for="event in pastEvents" :key="event.id" class="event">
            <h3 @click="goToEvent(event.id)" class="event-name">{{ event.name }}</h3>
            <p><strong>Address:</strong> {{ event.address }}</p>
            <p><strong>Date & Time:</strong> {{ formatDateTime(event.dateTime) }} - {{ formatDateTime(event.endTime) }}</p>
            <p><strong>Attendees:</strong> {{ event.attendees }}</p>
            <p><strong>Created by:</strong> {{ event.createdBy }}</p>
            <p>{{ event.description }}</p>
          </div>
        </div>
        <p v-else>You have no past events.</p>
      </div> -->
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { isLoggedIn, token } from '../store/user'
import { getJoinedEventsList, getCreatedEventsList, getEventInvitesList } from '../api/user'
import { joinEvent as joinEventAPI } from '../api/event'

const router = useRouter()
const route = useRoute()

const activeTab = ref('created')
// const joinedEvents = ref([])
const createdEvents = ref([])
// const eventInvitationsList = ref([])
//const pastEvents = computed(() => {
//  return [...joinedEvents.value, ...createdEvents.value].filter(event => new Date(event.end_datetime) < new Date())
//})

onMounted(async () => {
  if (!isLoggedIn.value) {
    router.push({ path: '/login', query: { redirect: route.fullPath } })
  } else {
    try {
      // joinedEvents.value = await getJoinedEventsList(token)
      createdEvents.value = await getCreatedEventsList(token)
      // eventInvitationsList.value = await getEventInvitesList(token)
    } catch (error) {
      console.error('Failed to fetch events:', error)
    }
  }
})

// const joinEvent = async (eventId) => {
//   const token = user.value.token
//   try {
//     await joinEventAPI(token, eventId)
//     joinedEvents.value = await getJoinedEventsList(token)
//     console.log(`Joined event with ID: ${eventId}`)
//   } catch (error) {
//     console.error('Failed to join event:', error)
//   }
// }

// const confirmJoinEvent = (eventId) => {
//   if (confirm('Are you sure you want to join this event?')) {
//     joinEvent(eventId)
//   }
// }

const leaveEvent = async (eventId) => {
  // ...existing code...
}

const confirmLeaveEvent = (eventId) => {
  // ...existing code...
}

const deleteEvent = async (eventId) => {
  // ...existing code...
}

const confirmDeleteEvent = (eventId) => {
  // ...existing code...
}

const editEvent = (eventId) => {
  router.push({ path: `/edit-event/${eventId}` })
}

const inviteSomeone = (eventId) => {
  console.log(`Inviting someone to event with ID: ${eventId}`)
  // Add logic to invite someone to the event
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
