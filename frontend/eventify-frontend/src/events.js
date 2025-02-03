import { ref } from 'vue'

export const events = ref([
  {
    id: 1,
    name: 'Music Concert',
    address: '123 Main St, New York, NY',
    dateTime: '2023-12-01 19:00',
    endTime: '2023-12-01 22:00',
    attendees: 150,
    description: 'Join us for an evening of live music and entertainment.',
    createdBy: 'Jane Doe',
  },
  {
    id: 2,
    name: 'Art Exhibition',
    address: '456 Elm St, Los Angeles, CA',
    dateTime: '2023-12-05 17:00',
    endTime: '2023-12-05 20:00',
    attendees: 200,
    description: 'Explore the latest art pieces from local artists.',
    createdBy: 'John Smith',
  },
  {
    id: 3,
    name: 'Tech Conference',
    address: '789 Pine St, San Francisco, CA',
    dateTime: '2023-12-10 09:00',
    endTime: '2023-12-10 17:00',
    attendees: 300,
    description: 'A conference discussing the latest trends in technology.',
    createdBy: 'John Smith',
  },
])

export const joinedEventIds = ref([])
export const eventInvitations = ref([])
