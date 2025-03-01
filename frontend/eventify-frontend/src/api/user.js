import axios from 'axios';
import Cookies from 'js-cookie';

const API_URL = 'https://app-eq-12-eventify-29bf10cbb7c2.herokuapp.com/api/user';

export const signup = async (userData) => {
  try {
    const response = await axios.post(`${API_URL}/signup/`, userData);
    
    return response.data;

  } catch (error) {
    if (error.response) {
      throw error.response.data;
    } else {
      throw { error: 'Network error or server is not responding' };
    }
  }
};

export const login = async (credentials) => {
  try {
    const response = await axios.post(`${API_URL}/login/`, credentials);
    
    // stocker le token dans un cookie avec durée de 7 jours et transmission 
    // sécurisée (https) seulement. 
    if (response.status === 200 && response.data.token) {
      Cookies.set('token', response.data.token, { expires: 7, secure: true });
    }
    
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const logout = async (token) => {
  try {
    const response = await axios.post(`${API_URL}/logout/`, {}, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const editProfile = async (token, profileData) => {
  try {
    const response = await axios.put(`${API_URL}/profile/edit/`, profileData, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const getProfileInfo = async (token) => {
  try {
    const response = await axios.get(`${API_URL}/profile/`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const getJoinedEventsList = async (token) => {
  try {
    const response = await axios.get(`${API_URL}/events/joined/`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const getEventInvitesList = async (token) => {
  try {
    const response = await axios.get(`${API_URL}/events/invitations/`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const getCreatedEventsList = async (token) => {
  try {
    const response = await axios.get(`${API_URL}/events/created/`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const getAllUsers = async (token) => {
  try {
    const response = await axios.get(`${API_URL}/all/`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};
