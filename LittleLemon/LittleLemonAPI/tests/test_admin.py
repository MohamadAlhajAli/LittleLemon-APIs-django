from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from LittleLemonAPI import models


class AdminAccessTests(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="test-password",
        )
        self.client.force_login(self.admin_user)

    def admin_url(self, model, action):
        return reverse(
            f"admin:{model._meta.app_label}_"
            f"{model._meta.model_name}_{action}"
        )

    def test_all_models_have_accessible_admin_lists(self):
        for model in (
            models.Category,
            models.MenuItem,
            models.Cart,
            models.Order,
            models.OrderItem,
        ):
            with self.subTest(model=model.__name__):
                response = self.client.get(
                    self.admin_url(model, "changelist")
                )

                self.assertEqual(response.status_code, 200)

    def test_catalog_add_pages_are_accessible(self):
        for model in (models.Category, models.MenuItem):
            with self.subTest(model=model.__name__):
                response = self.client.get(
                    self.admin_url(model, "add")
                )

                self.assertEqual(response.status_code, 200)

    def test_transaction_add_pages_are_forbidden(self):
        for model in (models.Cart, models.Order, models.OrderItem):
            with self.subTest(model=model.__name__):
                response = self.client.get(
                    self.admin_url(model, "add")
                )

                self.assertEqual(response.status_code, 403)
