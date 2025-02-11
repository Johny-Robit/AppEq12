# Documentation de l'API

# Appels API

## User
- **Signup** (POST) (Public)
- **Login** (Public)
- **Logout**
- **IsAuthenticated**
- **EditProfile** (PUT)
- **GetProfileInfo** (GET)
- **GetJoinedEventsList** (GET)  
  - // avoir la liste des évènements auxquels l’utilisateur a été invité
- **GetEventInvitesList** (GET)
- **GetCreatedEventsList** (GET)  
  - // avoir la liste des évènements que l’utilisateur a créés

## Event
- **JoinEvent** (PUT)
- **LeaveEvent** (PUT)
- **InviteToEvent** (PUT)
- **RemoveAttendee** (PUT) [Autorisation]
- **CreateEvent** (POST)
- **EditEvent** (PUT) [Autorisation]
- **DeleteEvent** (DELETE) [Autorisation]
- **GetEventInformations** (GET) (Public)
- **GetAttendeesList** (GET)  
  - // avoir la liste des personnes qui ont confirmé leur présence
- **GetPendingInvites** (GET)  
  - // avoir la liste des personnes qui doivent encore confirmer leur présence


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
    "message": "Login successful"
  }
  ```
- **Notes:**
  - Le serveur renvoie un cookie sessionid dans l'en-tête Set-Cookie.
  - Le cookie est HttpOnly, donc inaccessible en JavaScript (localStorage, sessionStorage).
  - Le client (navigateur, Postman, etc.) stocke le cookie automatiquement.
  - Toutes les requêtes suivantes incluront automatiquement ce cookie sans action du client.
  - Aucune information de session (sessionid) n'est retournée dans le body.


- **401 Unauthorized** (Si identifiants incorrects)
  ```json
  {
    "error": "Invalid credentials"
  }
  ```

### Logout (POST) (Authenticated)

**Endpoint:** `/api/user/logout/`

**Headers:** *(Les cookies sont envoyés automatiquement par le navigateur)*

Cookie: sessionid=<session_id>

**Response:**

- **200 OK**
  ```json
  {
    "message": "Logout successful"
  }
  ```

- **401 Unauthorized** (Si token invalide)

### Edit Profile (PUT) (Authenticated)

**Endpoint:** `/api/user/profile/edit/`

**Headers:**
```
Cookie: sessionid=<session_id>
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

### Get Profile Info (GET) (Authenticated)

**Endpoint:** `/api/user/profile/`

**Headers:**
```
Cookie: sessionid=<session_id>
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

### Get Joined Events List (GET) (Authenticated)

**Endpoint:** `/api/user/events/joined/`

**Headers:**
```
Cookie: sessionid=<session_id>
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

### Get Event Invites List (GET) (Authenticated)

**Endpoint:** `/api/user/events/invites/`

**Headers:**
```
Cookie: sessionid=<session_id>
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

### Get Created Events List (GET) (Authenticated)

**Endpoint:** `/api/user/events/created/`

**Headers:**
```
Cookie: sessionid=<session_id>
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

## Event API

### Join Event (PUT) (Authenticated)

**Endpoint:** `/api/event/join/`

**Headers:**
```
Cookie: sessionid=<session_id>
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

### Leave Event (PUT) (Authenticated)

**Endpoint:** `/api/event/leave/`

**Headers:**
```
Cookie: sessionid=<session_id>
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

### Invite to Event (PUT) (Authenticated, Owner Only)

**Endpoint:** `/api/event/invite/`

**Headers:**
```
Cookie: sessionid=<session_id>
```

**Body:**
```json
{
  "event_id": "integer",
  "user_id": "integer"
}
```

### Remove Attendee (PUT) (Authenticated, Owner Only)

**Endpoint:** `/api/event/remove_attendee/`

**Headers:**
```
Cookie: sessionid=<session_id>
```

**Body:**
```json
{
  "event_id": "integer",
  "user_id": "integer"
}
```

### Create Event (POST) (Authenticated)

**Endpoint:** `/api/event/create/`

**Headers:**
```
Cookie: sessionid=<session_id>
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

### Edit Event (PUT) (Authenticated, Owner Only)

**Endpoint:** `/api/event/edit/`

**Headers:**
```
Cookie: sessionid=<session_id>
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

### Delete Event (DELETE) (Authenticated, Owner Only)

**Endpoint:** `/api/event/delete/`

**Headers:**
```
Cookie: sessionid=<session_id>
```

**Body:**
```json
{
  "event_id": "integer"
}
```

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

### Get Attendees List (GET) (Authenticated)

**Endpoint:** `/api/event/{event_id}/attendees/`

**Headers:**
```
Cookie: sessionid=<session_id>
```

**Response:**
```json
[
  {
    "user_id": "integer"
  }
]
```

### Get Pending Invites (GET) (Authenticated, Owner Only)

**Endpoint:** `/api/event/{event_id}/pending_invites/`

**Headers:**
```
Cookie: sessionid=<session_id>
```

**Response:**
```json
[
  {
    "user_id": "integer"
  }
]
```


