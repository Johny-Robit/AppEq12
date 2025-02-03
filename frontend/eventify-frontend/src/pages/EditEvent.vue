<template>
  <div class="edit-event-container">
    <h1>Edit Event</h1>
    <form @submit.prevent="confirmUpdateEvent">
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
      <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
      <button type="submit">Update Event</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { events } from '../events.js'

const name = ref('')
const address = ref('')
const dateTime = ref('')
const endTime = ref('')
const description = ref('')
const errorMessage = ref('')

const router = useRouter()
const route = useRoute()
const eventId = route.params.id

onMounted(() => {
  const event = events.value.find(event => event.id === parseInt(eventId))
  if (event) {
    name.value = event.name
    address.value = event.address
    dateTime.value = event.dateTime
    endTime.value = event.endTime
    description.value = event.description
  } else {
    router.push('/my-events')
  }
})

const updateEvent = () => {
  if (new Date(endTime.value) <= new Date(dateTime.value)) {
    errorMessage.value = 'End date and time must be later than start date and time.'
    return
  }

  const event = events.value.find(event => event.id === parseInt(eventId))
  if (event) {
    event.name = name.value
    event.address = address.value
    event.dateTime = dateTime.value
    event.endTime = endTime.value
    event.description = description.value
    console.log('Event updated:', event)
    router.push('/my-events')
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

input, textarea {
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
