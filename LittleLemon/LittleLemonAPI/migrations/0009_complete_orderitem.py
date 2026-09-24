from decimal import Decimal

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("LittleLemonAPI", "0008_orderitem"),
    ]

    operations = [
        migrations.AddField(
            model_name="orderitem",
            name="order",
            field=models.ForeignKey(
                to="LittleLemonAPI.order",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="items",
            ),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="menuitem",
            field=models.ForeignKey(
                to="LittleLemonAPI.menuitem",
                on_delete=django.db.models.deletion.PROTECT,
            ),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="quantity",
            field=models.PositiveSmallIntegerField(),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="unit_price",
            field=models.DecimalField(
                max_digits=6,
                decimal_places=2,
            ),
        ),
        migrations.AddField(
            model_name="orderitem",
            name="price",
            field=models.DecimalField(
                max_digits=12,
                decimal_places=2,
            ),
        ),
        migrations.AddConstraint(
            model_name="orderitem",
            constraint=models.UniqueConstraint(
                fields=["order", "menuitem"],
                name="orderitem_unique_order_menuitem",
            ),
        ),
        migrations.AddConstraint(
            model_name="orderitem",
            constraint=models.CheckConstraint(
                condition=models.Q(
                    quantity__gte=1,
                    quantity__lte=100,
                ),
                name="orderitem_quantity_range",
            ),
        ),
        migrations.AddConstraint(
            model_name="orderitem",
            constraint=models.CheckConstraint(
                condition=models.Q(
                    unit_price__gte=Decimal("0.00"),
                    unit_price__lte=Decimal("9999.99"),
                ),
                name="orderitem_unit_price_range",
            ),
        ),
        migrations.AddConstraint(
            model_name="orderitem",
            constraint=models.CheckConstraint(
                condition=models.Q(price__gte=Decimal("0.00")),
                name="orderitem_price_nonnegative",
            ),
        ),
    ]