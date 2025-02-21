import { ref } from 'vue'
import { getProfileInfo } from '../api/user'

export const isLoggedIn = ref(!!localStorage.getItem('token'))
export const user = ref({ username: '', description: '' })

export const fetchUserProfile = async () => {
  const token = localStorage.getItem('token')
  if (isLoggedIn.value && token) {
    try {
      const response = await getProfileInfo(token)
      user.value = response
    } catch (error) {
      console.error('Failed to fetch profile info:', error)
      alert('Failed to fetch profile info')
    }
  }
}
