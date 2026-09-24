from django.contrib import admin

from LittleLemonAPI import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "slug")
    search_fields = ("title", "slug")


@admin.register(models.MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "featured", "category")
    list_filter = ("featured", "category")
    search_fields = ("title",)
    list_select_related = ("category",)


class ReadOnlyTransactionAdmin(admin.ModelAdmin):
    actions = None

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.Cart)
class CartAdmin(ReadOnlyTransactionAdmin):
    list_display = (
        "id", "user", "menuitem", "quantity", "unit_price", "price",
    )
    list_select_related = ("user", "menuitem")


@admin.register(models.Order)
class OrderAdmin(ReadOnlyTransactionAdmin):
    list_display = (
        "id", "user", "delivery_crew", "status", "total", "date",
    )
    list_filter = ("status", "date")
    list_select_related = ("user", "delivery_crew")


@admin.register(models.OrderItem)
class OrderItemAdmin(ReadOnlyTransactionAdmin):
    list_display = (
        "id", "order", "menuitem", "quantity", "unit_price", "price",
    )
    list_select_related = ("order", "menuitem")