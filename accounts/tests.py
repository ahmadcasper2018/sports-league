from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserViewSetTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="ahmad", password="1122")
        self.url = reverse("user-list")

    def valid_create_data(self):
        return {
            "username": "newuser",
            "password": "newpassword",
            "password_confirmation": "newpassword",
        }

    def test_valid_create_user(self):
        response = self.client.post(self.url, self.valid_create_data())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.last().username, "newuser")

    def test_invalid_create_user_as_existed(self):
        response = self.client.post(
            self.url,
            {"username": "ahmad", "password": "1122", "password_confirmation": "1122"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_create_user_no_passwords_match(self):
        response = self.client.post(
            self.url,
            {"username": "mark", "password": "1122", "password_confirmation": "1111"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.url = reverse("token_obtain_pair")

    def test_valid_user_login(self):
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertIn("username", response.data)

    def test_invalid_username_login(self):
        data = {"username": "invaliduser", "password": "testpassword"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_invalid_password_login(self):
        data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
