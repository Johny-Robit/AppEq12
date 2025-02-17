import { ref } from 'vue'

export const isLoggedIn = ref(false)

export const user = ref({
  username: 'JohnDoe420',
  email: 'john.doe@example.com',
  password: 'password123'
})
