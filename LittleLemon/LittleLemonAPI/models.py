from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone

# Create your models here.

class Category(models.Model): 
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True) 

    class Meta: 
        verbose_name_plural = "categories"

    def __str__(self): 
        return self.title

class MenuItem(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        db_index=True,
    )
    featured = models.BooleanField(default=False)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gte=0),
                name="menuitem_price_nonnegative",
            ),
            models.CheckConstraint(
                condition=models.Q(price__lte=Decimal("9999.99")),
                name="menuitem_price_maximum",
            ),
        ]
    
    def __str__(self): 
        return self.title

class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    menuitem = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "menuitem"],
                name="cart_unique_user_menuitem",
            ),
            models.CheckConstraint(
                condition=models.Q(quantity__gte=1, quantity__lte=100),
                name="cart_quantity_range",
            ),
            models.CheckConstraint(
                condition=models.Q(
                    unit_price__gte=Decimal("0.00"),
                    unit_price__lte=Decimal("9999.99"),
                ),
                name="cart_unit_price_range",
            ),
            models.CheckConstraint(
                condition=models.Q(price__gte=Decimal("0.00")),
                name="cart_price_nonnegative",
            ),
        ]

class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders",
    )
    delivery_crew = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="assigned_orders",
        null=True,
        blank=True,
    )
    status = models.BooleanField(default=False, db_index=True)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(
        default=timezone.localdate,
        db_index=True,
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(total__gte=Decimal("0.00")),
                name="order_total_nonnegative",
            ),
        ]

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    menuitem = models.ForeignKey(
        MenuItem,
        on_delete=models.PROTECT,
    )
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
    )
    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["order", "menuitem"],
                name="orderitem_unique_order_menuitem",
            ),
            models.CheckConstraint(
                condition=models.Q(
                    quantity__gte=1,
                    quantity__lte=100,
                ),
                name="orderitem_quantity_range",
            ),
            models.CheckConstraint(
                condition=models.Q(
                    unit_price__gte=Decimal("0.00"),
                    unit_price__lte=Decimal("9999.99"),
                ),
                name="orderitem_unit_price_range",
            ),
            models.CheckConstraint(
                condition=models.Q(price__gte=Decimal("0.00")),
                name="orderitem_price_nonnegative",
            ),
        ]
        











