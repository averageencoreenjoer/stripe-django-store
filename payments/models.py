from django.db import models
import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_SECRET_KEY


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='usd')

    def __str__(self):
        return self.name


class Discount(models.Model):
    name = models.CharField(max_length=100)
    percent = models.DecimalField(max_digits=5, decimal_places=2)
    stripe_coupon_id = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.stripe_coupon_id:
            coupon = stripe.Coupon.create(
                name=self.name,
                percent_off=float(self.percent),
                duration='once',
            )
            self.stripe_coupon_id = coupon.id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.percent}%)"


class Tax(models.Model):
    name = models.CharField(max_length=100)
    percent = models.DecimalField(max_digits=5, decimal_places=2)
    stripe_tax_rate_id = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.stripe_tax_rate_id:
            tax_rate = stripe.TaxRate.create(
                display_name=self.name,
                description=self.name,
                percentage=float(self.percent),
                inclusive=False,
            )
            self.stripe_tax_rate_id = tax_rate.id
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.percent}%)"


class Order(models.Model):
    objects = None
    items = models.ManyToManyField('Item')
    discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL)
    tax = models.ForeignKey(Tax, null=True, blank=True, on_delete=models.SET_NULL)

    def total_price(self):
        total = sum(item.price for item in self.items.all())
        if self.discount:
            total *= (1 - self.discount.percent / 100)
        if self.tax:
            total *= (1 + self.tax.percent / 100)
        return round(total, 2)

    def __str__(self):
        return f"Order #{self.pk}"

