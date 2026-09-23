from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.db.models.deletion import ProtectedError
from django.test import TestCase
from django.utils import timezone

from LittleLemonAPI import models

class CategoryModelTests(TestCase):
    def test_category_can_be_saved_and_loaded(self):
        category = models.Category.objects.create(
            title="Desserts",
            slug="desserts",
        )

        saved_category = models.Category.objects.get(pk=category.pk)

        self.assertEqual(saved_category.title, "Desserts")
        self.assertEqual(saved_category.slug, "desserts")

    def test_category_slug_must_be_unique(self):
        models.Category.objects.create(
            title="Desserts",
            slug="desserts",
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                models.Category.objects.create(
                    title="Sweet treats",
                    slug="desserts",
                )

    def test_category_string_representation_is_its_title(self):
        category = models.Category(
            title="Desserts",
            slug="desserts",
        )

        self.assertEqual(str(category), "Desserts")


class MenuItemModelTests(TestCase):
    def test_menu_item_can_be_saved_with_category(self):
        category = models.Category.objects.create(
            title="Main courses",
            slug="main-courses",
        )

        menu_item = models.MenuItem.objects.create(
            title="Grilled fish",
            price=Decimal("15.50"),
            category=category,
        )

        saved_item = models.MenuItem.objects.get(pk=menu_item.pk)

        self.assertEqual(saved_item.title, "Grilled fish")
        self.assertEqual(saved_item.price, Decimal("15.50"))
        self.assertEqual(saved_item.category_id, category.pk)
        self.assertFalse(saved_item.featured)

    def test_menu_item_price_cannot_be_negative(self):
        category = models.Category.objects.create(
            title="Main courses",
            slug="main-courses",
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                models.MenuItem.objects.create(
                    title="Grilled fish",
                    price=Decimal("-0.01"),
                    category=category,
                )

    def test_menu_item_price_cannot_exceed_limit(self):
        category = models.Category.objects.create(
            title="Main courses",
            slug="main-courses",
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                models.MenuItem.objects.create(
                    title="Grilled fish",
                    price=Decimal("10000.00"),
                    category=category,
                )

    def test_menu_item_string_representaion_is_its_title(self):
        menu_item = models.MenuItem(
            title = 'Grilled fish', 
            price = Decimal("15.50"), 
        )

        self.assertEqual(str(menu_item), 'Grilled fish')




