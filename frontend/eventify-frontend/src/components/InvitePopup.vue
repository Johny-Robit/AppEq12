<template>
  <div class="popup" v-if="visible">
    <div class="popup-content">
      <h2 class="popup-title">Invite Someone</h2>
      <input v-model="searchQuery" placeholder="Search users..." class="search-bar" />
      <div class="user-list-container">
        <ul>
          <li v-for="user in filteredUsers" :key="user.user_id" @click="inviteUser(user.user_id)" class="user-item">
            {{ user.username }}
          </li>
        </ul>
      </div>
      <div class="close-button-container">
        <button @click="closePopup" class="close-button">Close</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { inviteToEvent } from '../api/event'

const props = defineProps({
  visible: Boolean,
  users: Array,
  eventId: Number
})

const emit = defineEmits(['close'])

const searchQuery = ref('')

const sortedUsers = computed(() => {
  return [...props.users].sort((a, b) => a.username.localeCompare(b.username))
})

const filteredUsers = computed(() => {
  return sortedUsers.value.filter(user => 
    user.username.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const inviteUser = async (userId) => {
  try {
    const token = localStorage.getItem('token')
    await inviteToEvent(token, props.eventId, userId)
    alert('User invited successfully')
    emit('close')
  } catch (error) {
    console.error('Failed to invite user:', error)
    alert('Failed to invite user')
  }
}

const closePopup = () => {
  emit('close')
}
</script>

<style scoped>
.popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.popup-content {
  background: #343a40; /* Same color as NavBar background */
  padding: 4em; /* Twice the original padding */
  border-radius: 8px;
  text-align: center;
  color: white;
  width: 50%; /* Increase width */
  height: 60%;
  max-width: 600px; /* Set a max width */
  max-height: 800px; /* Set a max height */
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.popup-title {
  color: #42b983; /* Same green as the Events title */
}

.search-bar {
  width: 100%;
  padding: 0.5em;
  margin-bottom: 1em;
  border-radius: 4px;
  border: 1px solid #ccc;
  margin-top: 0; /* Move the search bar higher */
}

.user-list-container {
  border: 1px solid #495057; /* Add border around the list */
  border-radius: 4px;
  padding: 0.5em;
  max-height: 400px; /* Increase max height for scrolling */
  overflow-y: auto;
}

ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.user-item {
  cursor: pointer;
  padding: 0.5em 0;
  border-bottom: 1px solid #495057; /* Add border for demarcation */
}

.user-item:hover {
  background: #495057;
}

.close-button-container {
  display: flex;
  justify-content: center;
  margin-top: 1em;
}

.close-button {
  background-color: #42b983; /* Green color */
  color: white;
  border: none;
  padding: 0.5em 1em;
  cursor: pointer;
  border-radius: 4px;
}

.close-button:hover {
  background-color: #369f6b;
}
</style>
