import axios from 'axios';

const API_URL = 'http://localhost:8000/api/event'; // Ensure this points to the backend server address

export const joinEvent = async (token, eventId) => {
  try {
    const response = await axios.put(`${API_URL}/join/`, { event_id: eventId }, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const leaveEvent = async (token, eventId) => {
  try {
    const response = await axios.put(`${API_URL}/leave/`, { event_id: eventId }, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const inviteToEvent = async (token, eventId, userId) => {
  try {
    const response = await axios.put(`${API_URL}/invite/`, { event_id: eventId, user_id: userId }, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const removeAttendee = async (token, eventId, userId) => {
  try {
    const response = await axios.put(`${API_URL}/remove_attendee/`, { event_id: eventId, user_id: userId }, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const createEvent = async (token, eventData) => {
  try {
    const response = await axios.post(`${API_URL}/create/`, eventData, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const editEvent = async (token, eventData) => {
  try {
    const response = await axios.put(`${API_URL}/edit/`, eventData, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const deleteEvent = async (token, eventId) => {
  try {
    const response = await axios.delete(`${API_URL}/delete/`, {
      headers: { Authorization: `Bearer ${token}` },
      data: { event_id: eventId }
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const getEventInformation = async (eventId) => {
  try {
    const response = await axios.get(`${API_URL}/${eventId}/`);
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const getAttendeesList = async (token, eventId) => {
  try {
    const response = await axios.get(`${API_URL}/${eventId}/attendees/`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};

export const getPendingInvites = async (token, eventId) => {
  try {
    const response = await axios.get(`${API_URL}/${eventId}/pending_invites/`, {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data;
  } catch (error) {
    throw error.response.data;
  }
};
