from django.contrib import admin
from .models import Item, Order, Discount, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'currency')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_total', 'discount', 'tax', 'created_at')
    filter_horizontal = ('items',)


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount')


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('name', 'percent')
