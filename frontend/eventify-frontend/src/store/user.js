import { ref } from 'vue'
import Cookies from 'js-cookie'
import { getProfileInfo } from '../api/user'

export const isLoggedIn = ref(!!Cookies.get('token')) // Vérifie si un token existe
export const user = ref({ username: '', description: '' })

// fonction pour récupérer le token
export const getToken = () => {
  return Cookies.get('token') || null;
};

// fonction pour supprimer le token
export const removeToken = () => {
  Cookies.remove('token');
  localStorage.removeItem('username');
  isLoggedIn.value = false;
};

// fonction pour récupérer le profil de l'utilisateur
export const fetchUserProfile = async () => {
  const token = getToken(); // Récupère le token à partir du cookie

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
