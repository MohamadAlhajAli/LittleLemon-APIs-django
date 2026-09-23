from django.test import TestCase
from django.db import IntegrityError, transaction 

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