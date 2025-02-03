import { ref } from 'vue'

export const isLoggedIn = ref(false)

export const user = ref({
  name: 'John Doe',
  email: 'john.doe@example.com',
  password: 'password123'
})
