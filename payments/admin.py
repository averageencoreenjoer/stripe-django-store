from django.contrib import admin
from .models import Item, Order, Discount, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'currency']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id']
    filter_horizontal = ['items']


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['name', 'percent']
    exclude = ['stripe_coupon_id']


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ['name', 'percent']
    exclude = ['stripe_tax_rate_id']
