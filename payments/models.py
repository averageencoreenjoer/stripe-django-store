from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.IntegerField()
    currency = models.CharField(max_length=3, default='usd')

    def __str__(self):
        return self.name


class Order(models.Model):
    items = models.ManyToManyField(Item)


class Discount(models.Model):
    stripe_coupon_id = models.CharField(max_length=255)


class Tax(models.Model):
    stripe_tax_rate_id = models.CharField(max_length=255)
