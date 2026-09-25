from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


class RegistrationTests(APITestCase):
    def test_valid_registration_creates_normal_user(self):
        payload = {
            "username": "customer",
            "email": "customer@example.com",
            "password": "Lemon!River82Cloud",
        }

        response = self.client.post(
            "/api/users",
            data=payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        user = get_user_model().objects.get(
            username=payload["username"],
        )

        self.assertEqual(user.email, payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.groups.exists())
        self.assertNotIn("password", response.data)

    def test_registration_without_email_is_rejected(self):
        payload = {
            "username": "customer",
            "password": "Lemon!River82Cloud",
        }

        response = self.client.post(
            "/api/users",
            data=payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertIn("email", response.data)
        self.assertFalse(
            get_user_model().objects.filter(
                username=payload["username"],
            ).exists()
        )