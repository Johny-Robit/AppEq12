from django.test import TestCase
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

class AuthTestCase(APITestCase):
    """ Tests unitaires pour l'authentification """

    def setUp(self):
        """ Création d'un utilisateur de test """
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="testpassword")
        self.signup_url = "/api/user/signup/"
        self.login_url = "/api/user/login/"
        self.logout_url = "/api/user/logout/"
        self.auth_url = "/api/user/is-authenticated/"

    def test_signup(self):
        """ Test de l'inscription d'un utilisateur """
        data = {"username": "newuser", "email": "new@example.com", "password": "newpassword123"}
        response = self.client.post(self.signup_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_login(self):
        """ Test de connexion avec un utilisateur existant """
        data = {"email": "test@example.com", "password": "testpassword"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)  # Vérifie que le token est bien retourné
        
        # Stocker le token pour les requêtes authentifiées
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['token']}")

    def test_failed_login(self):
        """ Test d'échec de connexion avec un mauvais mot de passe """
        data = {"email": "test@example.com", "password": "wrongpassword"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_is_authenticated(self):
        """ Test si l'authentification est bien gérée """
        login_data = {"email": "test@example.com", "password": "testpassword"}
        login_response = self.client.post(self.login_url, login_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_response.data['token']}")
        
        response = self.client.get(self.auth_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["authenticated"], True)
        self.assertEqual(response.data["user"], "testuser")

    def test_logout(self):
        """ Test de déconnexion """
        login_data = {"email": "test@example.com", "password": "testpassword"}
        login_response = self.client.post(self.login_url, login_data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {login_response.data['token']}")
        
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Vérifier que l'utilisateur est bien déconnecté
        self.client.credentials()  # Supprime le token d'auth
        response = self.client.get(self.auth_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # Devrait être 401 Unauthorized
