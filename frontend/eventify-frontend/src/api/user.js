import axios from 'axios';

const API_URL = 'http://localhost:8000/api/user'; // Ensure this points to the backend server address

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
    const response = await axios.get(`${API_URL}/events/invites/`, {
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
