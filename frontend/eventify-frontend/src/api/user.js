import axios from 'axios';
import Cookies from 'js-cookie';

const API_URL = 'https://app-eq-12-eventify-29bf10cbb7c2.herokuapp.com/api/user';

const getCSRFToken = () => Cookies.get('csrftoken');

export const signup = async (userData) => {
  try {
    const response = await axios.post(`${API_URL}/signup/`, userData, {
      headers: { 'X-CSRFToken': getCSRFToken() },
    });
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
    const response = await axios.post(`${API_URL}/login/`, credentials, {
      headers: { 'X-CSRFToken': getCSRFToken() },
      withCredentials: true,
    });
    
    if (response.status === 200 && response.data.token) {
      const expirationTime = 1 / 48; // 30 minutes in days
      Cookies.set('token', response.data.token, { expires: expirationTime, secure: true, httpOnly: true });
      Cookies.set('refresh_token', response.data.refresh_token, { expires: 7, secure: true, httpOnly: true });
    }
    
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const refreshAccessToken = async () => {
  const refreshToken = Cookies.get('refresh_token');
  if (!refreshToken) {
    console.error('No refresh token found.');
    return null;
  }

  try {
    const response = await axios.post(`${API_URL}/token/refresh/`, { refresh: refreshToken });
    if (response.status === 200 && response.data.token) {
      Cookies.set('token', response.data.token, { expires: 7, secure: true, httpOnly: true });
      return response.data.token;
    }
  } catch (error) {
    console.error('Failed to refresh access token:', error);
    return null;
  }
}

export const logout = async (token) => {
  try {
    const response = await axios.post(`${API_URL}/logout/`, {}, {
      headers: { 
        Authorization: `Bearer ${token}`,
      },
      withCredentials: true,
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const editProfile = async (token, profileData) => {
  try {
    const response = await axios.put(`${API_URL}/profile/edit/`, profileData, {
      headers: { 
        Authorization: `Bearer ${token}`,
        'X-CSRFToken': getCSRFToken(),
      },
      withCredentials: true,
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const getProfileInfo = async (token) => {
  try {
    const response = await axios.get(`${API_URL}/profile/`, {
      headers: { 
        Authorization: `Bearer ${token}`,
      },
      withCredentials: true,
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const getJoinedEventsList = async (token) => {
  try {
    const response = await axios.get(`${API_URL}/events/joined/`, {
      headers: { 
        Authorization: `Bearer ${token}`,
      },
      withCredentials: true,
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const getEventInvitesList = async (token) => {
  try {
    const response = await axios.get(`${API_URL}/events/invitations/`, {
      headers: { 
        Authorization: `Bearer ${token}`,
      },
      withCredentials: true,
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const getCreatedEventsList = async (token) => {
  try {
    const response = await axios.get(`${API_URL}/events/created/`, {
      headers: { 
        Authorization: `Bearer ${token}`,
      },
      withCredentials: true,
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const getAllUsers = async (token) => {
  try {
    const response = await axios.get(`${API_URL}/all/`, {
      headers: { 
        Authorization: `Bearer ${token}`,
      },
      withCredentials: true,
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};
