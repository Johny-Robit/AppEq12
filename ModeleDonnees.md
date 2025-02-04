
# Modèle de Données

## User

- **UserID** *(Primary Key)* → Identifiant unique de l'utilisateur
- **Username** *(Unique)* → Nom d'utilisateur unique
- **Email** *(Unique)* → Adresse email unique
- **Password** *(Hashed)* → Mot de passe stocké sous forme chiffrée
- **Description** *(String)* → Description optionnelle de l'utilisateur
- **ProfileImageLink** *(Optionnel)* → Lien vers l'image de profil

## Django auth_user

- **password** *(Hashed)* → Mot de passe sécurisé
- **token** → Jeton d'authentification
- **username** *(FK: UserID)* → Référence vers l'utilisateur

## Event

- **EventID** *(Primary Key)* → Identifiant unique de l'événement
- **EventName** *(String)* → Nom de l'événement
- **EventAddress** *(String)* → Adresse de l'événement
- **StartDatetime** *(Datetime)* → Date et heure de début
- **EndDatetime** *(Datetime)* → Date et heure de fin
- **Description** *(String)* → Description de l'événement
- **EventIsPublic** *(Bool)* → Indique si l'événement est public ou privé
- **EventImageLink** *(Optionnel)* → Lien vers l'image de l'événement
- **PendingInvite** *(FK: UserID)* → Référence vers les utilisateurs invités en attente
- **OwnerID** *(FK: UserID)* → Référence vers l'utilisateur qui a créé l'événement
- **AttendeeID** *(FK: UserID)* → Référence vers les participants confirmés de l'événement


