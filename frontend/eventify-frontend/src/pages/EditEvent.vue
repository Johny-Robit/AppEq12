<template>
  <div class="edit-event-container" v-if="event">
    <h1>Edit Event</h1>
    <form @submit.prevent="confirmUpdateEvent">
      <div class="form-group">
        <label for="name">Event Name:</label>
        <input type="text" v-model="event.event_name" required />
      </div>
      <div class="form-group">
        <label for="address">Address:</label>
        <input type="text" v-model="event.event_address" required />
      </div>
      <div class="form-group">
        <label for="start_datetime">Start Date & Time:</label>
        <input type="datetime-local" v-model="event.start_datetime" required />
      </div>
      <div class="form-group">
        <label for="end_datetime">End Date & Time:</label>
        <input type="datetime-local" v-model="event.end_datetime" required />
      </div>
      <div class="form-group">
        <label for="description">Description:</label>
        <textarea v-model="event.description" required></textarea>
      </div>
      <div class="form-group">
        <label for="is_public">Event Visibility:</label>
        <input type="checkbox" v-model="event.is_public" /> Public
      </div>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      <button type="submit">Update Event</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getEventInformation, editEvent as editEventAPI } from '../api/event'
import { isLoggedIn, getToken } from '../store/user'

const event = ref(null)
const errorMessage = ref('')

const router = useRouter()
const route = useRoute()
const eventId = route.params.id

const fetchEvent = async () => {
  try {
    const response = await getEventInformation(eventId)
    event.value = response
  } catch (error) {
    console.error('Failed to fetch event information:', error)
    router.push('/my-events')
  }
}

onMounted(() => {
  if (!isLoggedIn.value) {
    router.push('/login')
  } else {
    fetchEvent()
  }
})

const updateEvent = async () => {
  if (new Date(event.value.end_datetime) <= new Date(event.value.start_datetime)) {
    errorMessage.value = 'End date and time must be later than start date and time.'
    return
  }

  try {
    const token = getToken()
    await editEventAPI(token, event.value)
    router.push('/my-events')
  } catch (error) {
    console.error('Failed to update event:', error)
    errorMessage.value = 'Failed to update event. Please try again.'
  }
}

const confirmUpdateEvent = () => {
  if (confirm('Are you sure you want to update this event?')) {
    updateEvent()
  }
}
</script>

<style scoped>
.edit-event-container {
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

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 1em;
}

label {
  margin-bottom: 0.5em;
}

input, textarea, select {
  padding: 0.5em;
  border: 1px solid #ccc;
  border-radius: 4px;
}

button {
  padding: 0.5em 1em;
  border: none;
  border-radius: 4px;
  background-color: #42b983;
  color: white;
  cursor: pointer;
}

button:hover {
  background-color: #369f6b;
}

.error {
  color: red;
  margin-bottom: 1em;
}
</style>
