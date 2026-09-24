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


class CartModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="customer",
        )
        self.category = models.Category.objects.create(
            title="Main courses",
            slug="main-courses",
        )
        self.menu_item = models.MenuItem.objects.create(
            title="Grilled fish",
            price=Decimal("15.50"),
            category=self.category,
        )

    def make_cart(self, **overrides):
        values = {
            "user": self.user,
            "menuitem": self.menu_item,
            "quantity": 2,
            "unit_price": Decimal("15.50"),
            "price": Decimal("31.00"),
        }
        values.update(overrides)
        return models.Cart.objects.create(**values)

    def test_cart_can_be_saved_and_loaded(self):
        cart = self.make_cart()
        cart.refresh_from_db()

        self.assertEqual(cart.user_id, self.user.pk)
        self.assertEqual(cart.menuitem_id, self.menu_item.pk)
        self.assertEqual(cart.quantity, 2)
        self.assertEqual(cart.unit_price, Decimal("15.50"))
        self.assertEqual(cart.price, Decimal("31.00"))

    def test_user_cannot_have_duplicate_menu_item_rows(self):
        self.make_cart()

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.make_cart()

    def test_other_users_can_add_the_same_menu_item(self):
        self.make_cart()
        other_user = get_user_model().objects.create_user(
            username="other-customer",
        )

        other_cart = self.make_cart(user=other_user)

        self.assertEqual(other_cart.user_id, other_user.pk)
        self.assertEqual(models.Cart.objects.count(), 2)

    def test_invalid_values_are_rejected(self):
        invalid_values = [
            ("quantity", -1),
            ("quantity", 0),
            ("quantity", 101),
            ("unit_price", Decimal("-0.01")),
            ("unit_price", Decimal("10000.00")),
            ("price", Decimal("-0.01")),
        ]

        for field, value in invalid_values:
            with self.subTest(field=field, value=value):
                with self.assertRaises(IntegrityError):
                    with transaction.atomic():
                        self.make_cart(**{field: value})

    def test_valid_boundaries_are_supported(self):
        valid_values = [
            (1, Decimal("0.00"), Decimal("0.00")),
            (100, Decimal("9999.99"), Decimal("999999.00")),
        ]

        for quantity, unit_price, price in valid_values:
            with self.subTest(quantity=quantity):
                cart = self.make_cart(
                    quantity=quantity,
                    unit_price=unit_price,
                    price=price,
                )
                cart.refresh_from_db()

                self.assertEqual(cart.quantity, quantity)
                self.assertEqual(cart.unit_price, unit_price)
                self.assertEqual(cart.price, price)

                cart.delete()

    def test_deleting_user_removes_their_cart(self):
        cart = self.make_cart()
        cart_id = cart.pk

        self.user.delete()

        self.assertFalse(models.Cart.objects.filter(pk=cart_id).exists())

    def test_deleting_menu_item_removes_its_cart_rows(self):
        cart = self.make_cart()
        cart_id = cart.pk

        self.menu_item.delete()

        self.assertFalse(models.Cart.objects.filter(pk=cart_id).exists())


class OrderModelTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="customer",
        )
        self.crew = get_user_model().objects.create_user(
            username="courier",
        )

    def make_order(self, **overrides):
        values = {
            "user": self.user,
            "total": Decimal("31.00"),
        }
        values.update(overrides)
        return models.Order.objects.create(**values)

    def test_new_order_has_expected_defaults(self):
        order = self.make_order()
        order.refresh_from_db()

        self.assertEqual(order.user_id, self.user.pk)
        self.assertEqual(order.total, Decimal("31.00"))
        self.assertFalse(order.status)
        self.assertIsNone(order.delivery_crew)
        self.assertEqual(order.date, timezone.localdate())

    def test_order_can_be_assigned_to_delivery_user(self):
        order = self.make_order(delivery_crew=self.crew)
        order.refresh_from_db()

        self.assertEqual(order.delivery_crew_id, self.crew.pk)
        self.assertEqual(self.user.orders.get(pk=order.pk), order)
        self.assertEqual(
            self.crew.assigned_orders.get(pk=order.pk),
            order,
        )

    def test_zero_and_large_totals_are_supported(self):
        for amount in (Decimal("0.00"), Decimal("99999900.00")):
            with self.subTest(amount=amount):
                order = self.make_order(total=amount)
                order.refresh_from_db()

                self.assertEqual(order.total, amount)

    def test_total_cannot_be_negative(self):
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.make_order(total=Decimal("-0.01"))

    def test_order_owner_cannot_be_deleted(self):
        order = self.make_order()

        with self.assertRaises(ProtectedError):
            self.user.delete()

        self.assertTrue(
            models.Order.objects.filter(pk=order.pk).exists()
        )
        self.assertTrue(
            get_user_model().objects.filter(pk=self.user.pk).exists()
        )

    def test_deleting_delivery_user_clears_assignment(self):
        order = self.make_order(delivery_crew=self.crew)

        self.crew.delete()
        order.refresh_from_db()

        self.assertIsNone(order.delivery_crew)
        self.assertEqual(order.user_id, self.user.pk)
        self.assertEqual(order.total, Decimal("31.00"))

    def test_deleting_order_preserves_both_users(self):
        order = self.make_order(delivery_crew=self.crew)
        order_id = order.pk

        order.delete()

        self.assertFalse(
            models.Order.objects.filter(pk=order_id).exists()
        )
        self.assertTrue(
            get_user_model().objects.filter(pk=self.user.pk).exists()
        )
        self.assertTrue(
            get_user_model().objects.filter(pk=self.crew.pk).exists()
        )


class OrderItemModelTests(TestCase): 
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="customer",
        )
        self.category = models.Category.objects.create(
            title="Main courses",
            slug="main-courses",
        )
        self.menu_item = models.MenuItem.objects.create(
            title="Grilled fish",
            price=Decimal("15.50"),
            category=self.category,
        )
        self.order = models.Order.objects.create(
            user=self.user,
            total=Decimal("31.00"),
        )

    def make_order_item(self, **overrides):
        values = {
            "order": self.order,
            "menuitem": self.menu_item,
            "quantity": 2,
            "unit_price": Decimal("15.50"),
            "price": Decimal("31.00"),
        }
        values.update(overrides)
        return models.OrderItem.objects.create(**values)

    def test_order_item_can_be_saved_and_loaded(self):
        item = self.make_order_item()

        saved = models.OrderItem.objects.get(pk=item.pk)

        self.assertEqual(saved.order, self.order)
        self.assertEqual(saved.menuitem, self.menu_item)
        self.assertEqual(saved.quantity, 2)
        self.assertEqual(saved.unit_price, Decimal("15.50"))
        self.assertEqual(saved.price, Decimal("31.00"))
        self.assertEqual(self.order.items.get(), saved)

    def test_menu_item_must_be_unique_within_order(self):
        self.make_order_item()

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                self.make_order_item()
    
    def test_same_menu_item_can_appear_in_different_orders(self):
        first_item = self.make_order_item()
        other_order = models.Order.objects.create(
            user=self.user,
            total=Decimal("31.00"),
        )

        second_item = self.make_order_item(order=other_order)

        self.assertNotEqual(first_item.pk, second_item.pk)
        self.assertEqual(first_item.menuitem, second_item.menuitem)

   


        self.assertTrue(
            models.Order.objects.filter(pk=order.pk).exists()
        )
        self.assertTrue(
            get_user_model().objects.filter(pk=self.user.pk).exists()
        )

    def test_deleting_delivery_user_clears_assignment(self):
        order = self.make_order(delivery_crew=self.crew)

        self.crew.delete()
        order.refresh_from_db()

        self.assertIsNone(order.delivery_crew)
        self.assertEqual(order.user_id, self.user.pk)
        self.assertEqual(order.total, Decimal("31.00"))

    def test_deleting_order_preserves_both_users(self):
        order = self.make_order(delivery_crew=self.crew)
        order_id = order.pk

        order.delete()

        self.assertFalse(
            models.Order.objects.filter(pk=order_id).exists()
        )
        self.assertTrue(
            get_user_model().objects.filter(pk=self.user.pk).exists()
        )
        self.assertTrue(
            get_user_model().objects.filter(pk=self.crew.pk).exists()
        )
