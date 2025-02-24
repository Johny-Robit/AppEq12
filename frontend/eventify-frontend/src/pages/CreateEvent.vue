<template>
  <div class="create-event-container">
    <h1>Create an Event</h1>
    <form @submit.prevent="confirmCreateEvent">
      <div class="form-group">
        <label for="name">Event Name:</label>
        <input type="text" v-model="name" required />
      </div>
      <div class="form-group">
        <label for="address">Address:</label>
        <input type="text" v-model="address" required />
      </div>
      <div class="form-group">
        <label for="dateTime">Date & Time:</label>
        <input type="datetime-local" v-model="dateTime" required />
      </div>
      <div class="form-group">
        <label for="endTime">End Time:</label>
        <input type="datetime-local" v-model="endTime" required />
      </div>
      <div class="form-group">
        <label for="description">Description:</label>
        <textarea v-model="description" required></textarea>
      </div>
      <div class="form-group">
        <label for="isPrivate">Private Event:</label>
        <input type="checkbox" v-model="isPrivate" />
      </div>
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      <div class="buttons">
        <button type="submit">Create Event</button>
        <button type="button" @click="confirmCancelEvent">Cancel</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { isLoggedIn } from '../store/user'
import { createEvent as createEventAPI } from '../api/event'

const name = ref('')
const address = ref('')
const dateTime = ref('')
const endTime = ref('')
const description = ref('')
const isPrivate = ref(false)
const errorMessage = ref('')

const isPublic = computed(() => !isPrivate.value)

const router = useRouter()
const route = useRoute()

onMounted(() => {
  if (!isLoggedIn.value) {
    router.push({ path: '/login', query: { redirect: route.fullPath } })
  }
})

const createEvent = async () => {
  if (new Date(endTime.value) <= new Date(dateTime.value)) {
    errorMessage.value = 'End date and time must be later than start date and time.'
    return
  }

  const newEvent = {
    event_name: name.value,
    event_address: address.value,
    start_datetime: dateTime.value,
    end_datetime: endTime.value,
    description: description.value,
    is_public: isPublic.value
  }

  const token = localStorage.getItem('token')
  try {
    await createEventAPI(token, newEvent)
    router.push('/events')
  } catch (error) {
    errorMessage.value = 'Failed to create event: ' + error.message
    console.error('Failed to create event:', error)
  }
}

const confirmCreateEvent = () => {
  if (confirm('Are you sure you want to create this event?')) {
    createEvent()
  }
}

const confirmCancelEvent = () => {
  if (confirm('Are you sure you want to cancel creating this event?')) {
    router.push('/events')
  }
}
</script>

<style scoped>
.create-event-container {
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

input, textarea {
  padding: 0.5em;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.buttons {
  display: flex;
  justify-content: center;
  gap: 1em;
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
