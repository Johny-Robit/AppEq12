# GLO3202_AppWeb_eq12

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

## Event API

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

