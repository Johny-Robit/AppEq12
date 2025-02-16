from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

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
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Logged in successfully", response.data["success"])  # Vérifie le message retourné

    def test_failed_login(self):
        """ Test d'échec de connexion avec un mauvais mot de passe """
        data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid credentials", response.data["error"])

    def test_is_authenticated(self):
        """ Test si l'authentification est bien gérée """
        self.client.login(username="testuser", password="testpassword")  # Connexion utilisateur
        response = self.client.get(self.auth_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["authenticated"], True)
        self.assertEqual(response.data["user"], "testuser")

    def test_logout(self):
        """ Test de déconnexion """
        self.client.login(username="testuser", password="testpassword")  # Connexion
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Vérifier que l'utilisateur est bien déconnecté
        response = self.client.get(self.auth_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["authenticated"], False)  # Doit retourner `authenticated: False`
