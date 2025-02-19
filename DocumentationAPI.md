# Documentation de l'API

# Appels API

## User
- [**Signup**](#signup-post-public) (POST) (Public)
- [**Login**](#login-post-public) (Public)
- [**Logout**](#logout-post-authenticated)
- [**EditProfile**](#edit-profile-put-authenticated) (PUT)
- [**GetProfileInfo**](#get-profile-info-get-authenticated) (GET)
- [**GetJoinedEventsList**](#get-joined-events-list-get-authenticated) (GET)  
  - // avoir la liste des évènements que l'utilisateur a rejoint
- [**GetUserInvitations**](#get-user-invitations-list-get-authenticated) (GET)
  - // avoir la liste des évènements auxquels l’utilisateur a été invité
- [**GetCreatedEventsList**](#get-created-events-list-get-authenticated) (GET)  
  - // avoir la liste des évènements que l’utilisateur a créés

## Event
- [**JoinEvent**](#join-event-put-authenticated) (PUT)
- [**LeaveEvent**](#leave-event-put-authenticated) (PUT)
- [**InviteToEvent**](#invite-to-event-put-authenticated-owner-only) (PUT)
- [**RemoveAttendee**](#remove-attendee-put-authenticated-owner-only) (PUT) [Autorisation]
- [**CreateEvent**](#create-event-post-authenticated) (POST)
- [**EditEvent**](#edit-event-put-authenticated-owner-only) (PUT) [Autorisation]
- [**DeleteEvent**](#delete-event-delete-authenticated-owner-only) (DELETE) [Autorisation]
- [**GetEventInformations**](#get-event-information-get-public) (GET) (Public)
- [**GetAttendeesList**](#get-attendees-list-get-authenticated) (GET)  
  - // avoir la liste des personnes qui ont confirmé leur présence
- [**GetPendingInvites**](#get-pending-invites-get-authenticated-owner-only) (GET)  
  - // avoir la liste des personnes qui doivent encore confirmer leur présence

---

## User API

### Signup (POST) (Public)

**Endpoint:** `/api/user/signup/`

**Body:**
```json
{
  "username": "string",
  "email": "string",
  "password": "string"
}
```

**Response:**

- **201 Created**
  ```json
  {
    "message": "User created successfully",
    "user_id": "integer"
  }
  ```

- **400 Bad Request** (Si email ou username déjà utilisé)
  ```json
  {
    "error": "Email or username already taken"
  }
  ```

---

### Login (POST) (Public)

**Endpoint:** `/api/user/login/`

**Body:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Response:**

- **200 OK**
  ```json
  {
    "token": "string"
  }
  ```

- **401 Unauthorized** (Si identifiants incorrects)
  ```json
  {
    "error": "Invalid credentials"
  }
  ```

---

### Logout (POST) (Authenticated)

**Endpoint:** `/api/user/logout/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**

- **200 OK**
  ```json
  {
    "message": "Logout successful"
  }
  ```

- **401 Unauthorized** (Si token invalide)

---

### Edit Profile (PUT) (Authenticated)

**Endpoint:** `/api/user/profile/edit/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Body:**
```json
{
  "description": "string",
  "profile_image_link": "string"
}
```

**Response:**

- **200 OK**
  ```json
  {
    "message": "Profile updated successfully"
  }
  ```

- **400 Bad Request** (Si problème de validation)

---

### Get Profile Info (GET) (Authenticated)

**Endpoint:** `/api/user/profile/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**

- **200 OK**
  ```json
  {
    "username": "string",
    "description": "string",
    "profile_image_link": "string"
  }
  ```

- **404 Not Found** (Si utilisateur non trouvé)

---

### Get Joined Events List (GET) (Authenticated)

**Endpoint:** `/api/user/events/joined/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
[
  {
    "event_id": "integer",
    "event_name": "string",
    "event_address": "string",
    "start_datetime": "string",
    "end_datetime": "string",
    "Owner_id": "integer"
  }
]
```

---

### Get Event Invites List (GET) (Authenticated)

**Endpoint:** `/api/user/events/invites/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
[
  {
    "event_id": "integer",
    "event_name": "string",
    "event_address": "string",
    "start_datetime": "string",
    "end_datetime": "string",
    "Owner_id": "integer"
  }
]
```

---

### Get Created Events List (GET) (Authenticated)

**Endpoint:** `/api/user/events/created/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
[
  {
    "event_id": "integer",
    "event_name": "string",
    "event_address": "string",
    "start_datetime": "string",
    "end_datetime": "string",
    "Owner_id": "integer"
  }
]
```

---

## Event API

---

### Join Event (PUT) (Authenticated)

**Endpoint:** `/api/event/join/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Body:**
```json
{
  "event_id": "integer"
}
```

**Response:**

- **200 OK**
  ```json
  {
    "message": "Joined event successfully"
  }
  ```

- **404 Not Found** (Si l'événement n'existe pas)
  ```json
  {
    "error": "Event not found"
  }
  ```

- **400 Bad Request** (Si l'utilisateur est déjà inscrit)
  ```json
  {
    "error": "User already joined the event"
  }
  ```

---

### Leave Event (PUT) (Authenticated)

**Endpoint:** `/api/event/leave/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Body:**
```json
{
  "event_id": "integer"
}
```

**Response:**

- **200 OK**
  ```json
  {
    "message": "Left event successfully"
  }
  ```

- **400 Bad Request** (Si l'utilisateur n'est pas inscrit à l'événement)
  ```json
  {
    "error": "User is not part of the event"
  }
  ```

---

### Invite to Event (PUT) (Authenticated, Owner Only)

**Endpoint:** `/api/event/invite/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Body:**
```json
{
  "event_id": "integer",
  "user_id": "integer"
}
```

---

### Remove Attendee (PUT) (Authenticated, Owner Only)

**Endpoint:** `/api/event/remove_attendee/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Body:**
```json
{
  "event_id": "integer",
  "user_id": "integer"
}
```

---

### Create Event (POST) (Authenticated)

**Endpoint:** `/api/event/create/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Body:**
```json
{
  "event_name": "string",
  "event_address": "string",
  "start_datetime": "string",
  "end_datetime": "string",
  "description": "string",
  "is_public": "boolean",
  "event_image_link": "string"
}
```

**Response:**

- **201 Created**
  ```json
  {
    "message": "Event created successfully",
    "event_id": "integer"
  }
  ```

- **400 Bad Request** (Si données invalides)
  ```json
  {
    "error": "Invalid input data"
  }
  ```

---

### Edit Event (PUT) (Authenticated, Owner Only)

**Endpoint:** `/api/event/edit/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Body:**
```json
{
  "event_id": "integer",
  "event_name": "string",
  "event_address": "string",
  "start_datetime": "string",
  "end_datetime": "string",
  "description": "string",
  "is_public": "boolean"
}
``` 

---

### Delete Event (DELETE) (Authenticated, Owner Only)

**Endpoint:** `/api/event/delete/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Body:**
```json
{
  "event_id": "integer"
}
```

---

### Get Event Information (GET) (Public)

**Endpoint:** `/api/event/{event_id}/`

**Response:**

- **200 OK**
  ```json
  {
    "ownerID": "integer",
    "event_name": "string",
    "event_address": "string",
    "start_datetime": "string",
    "end_datetime": "string",
    "description": "string",
    "is_public": "boolean"
  }
  ```

- **404 Not Found** (Si l'événement n'existe pas)
  ```json
  {
    "error": "Event not found"
  }
  ```

---

### Get Attendees List (GET) (Authenticated)

**Endpoint:** `/api/event/{event_id}/attendees/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
[
  {
    "user_id": "integer"
  }
]
```

---

### Get Pending Invites (GET) (Authenticated, Owner Only)

**Endpoint:** `/api/event/{event_id}/pending_invites/`

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response:**
```json
[
  {
    "user_id": "integer"
  }
]
```


