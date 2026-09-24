from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from decimal import Decimal 

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


    # -------------------
    def make_transaction_records(self):
        category = models.Category.objects.create(
            title="Main courses",
            slug="main-courses",
        )
        menu_item = models.MenuItem.objects.create(
            title="Grilled fish",
            price=Decimal("15.50"),
            category=category,
        )
        order = models.Order.objects.create(
            user=self.admin_user,
            total=Decimal("31.00"),
        )
        cart = models.Cart.objects.create(
            user=self.admin_user,
            menuitem=menu_item,
            quantity=2,
            unit_price=Decimal("15.50"),
            price=Decimal("31.00"),
        )
        order_item = models.OrderItem.objects.create(
            order=order,
            menuitem=menu_item,
            quantity=2,
            unit_price=Decimal("15.50"),
            price=Decimal("31.00"),
        )
        return cart, order, order_item


    def test_transaction_detail_pages_are_viewable(self):
        for record in self.make_transaction_records():
            model = type(record)

            with self.subTest(model=model.__name__):
                url = reverse(
                    f"admin:{model._meta.app_label}_"
                    f"{model._meta.model_name}_change",
                    args=[record.pk],
                )

                response = self.client.get(url)

                self.assertEqual(response.status_code, 200)

    def test_transaction_edit_requests_are_forbidden(self):
        for record in self.make_transaction_records():
            model = type(record)

            with self.subTest(model=model.__name__):
                url = reverse(
                    f"admin:{model._meta.app_label}_"
                    f"{model._meta.model_name}_change",
                    args=[record.pk],
                )

                if isinstance(record, models.Order):
                    changes = {"total": "99.00"}
                    field = "total"
                else:
                    changes = {"price": "99.00"}
                    field = "price"

                original_value = getattr(record, field)

                response = self.client.post(url, data=changes)

                self.assertEqual(response.status_code, 403)
                record.refresh_from_db()
                self.assertEqual(getattr(record, field), original_value)

    def test_transaction_delete_requests_are_forbidden(self):
        for record in self.make_transaction_records():
            model = type(record)

            with self.subTest(model=model.__name__):
                url = reverse(
                    f"admin:{model._meta.app_label}_"
                    f"{model._meta.model_name}_delete",
                    args=[record.pk],
                )

                response = self.client.post(url, data={"post": "yes"})

                self.assertEqual(response.status_code, 403)
                self.assertTrue(
                    model.objects.filter(pk=record.pk).exists()
                )






