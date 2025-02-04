# Documentation de l'API

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
    "token": "string"
  }
  ```

- **401 Unauthorized** (Si identifiants incorrects)
  ```json
  {
    "error": "Invalid credentials"
  }
  ```

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

## Event API

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

