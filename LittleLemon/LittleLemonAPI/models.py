from django.db import models
from decimal import Decimal 

# Create your models here.

class Category(models.Model): 
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True) 

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
















