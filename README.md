# GLO3202_AppWeb_eq12

# Signup - Création d'un utilisateur

## Endpoint
`POST /api/user/signup/`

## Accès
Public (aucune authentification requise)

## Requête

### Headers
Aucun

### Body (JSON)
```json
{
  "username": "john_doe",
  "email": "john.doe@example.com",
  "password": "mypassword123"
}
