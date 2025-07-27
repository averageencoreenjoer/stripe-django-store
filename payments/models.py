from django.db import models


class Item(models.Model):
    CURRENCIES = [
        ('usd', 'USD'),
        ('eur', 'EUR'),
    ]
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCIES, default='usd')

    def __str__(self):
        return self.name


class Discount(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # фиксированная скидка в валюте

    def __str__(self):
        return f"{self.name} - {self.amount}"


class Tax(models.Model):
    name = models.CharField(max_length=100)
    percent = models.DecimalField(max_digits=5, decimal_places=2)  # налог в процентах, например 7.25

    def __str__(self):
        return f"{self.name} - {self.percent}%"


class Order(models.Model):
    items = models.ManyToManyField(Item)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, blank=True)
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_items_total(self):
        return sum(item.price for item in self.items.all())

    def get_discount_amount(self):
        return self.discount.amount if self.discount else 0

    def get_tax_amount(self):
        subtotal = self.get_items_total() - self.get_discount_amount()
        if self.tax:
            return subtotal * self.tax.percent / 100
        return 0

    def get_total(self):
        return max(self.get_items_total() - self.get_discount_amount() + self.get_tax_amount(), 0)

    def get_currency(self):
        first_item = self.items.first()
        if first_item:
            return first_item.currency
        return 'usd'

    def __str__(self):
        return f"Order #{self.id} - {self.get_total()} {self.get_currency().upper()}"
