import os

import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from .models import Item, Order

stripe.api_key = settings.STRIPE_SECRET_KEY


def item_detail(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'item_detail.html', {
        'item': item,
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
    })


def buy_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': item.currency,
                'unit_amount': int(item.price * 100),
                'product_data': {'name': item.name},
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://example.com/success',
        cancel_url='https://example.com/cancel',
    )
    return JsonResponse({'id': session.id})


def order_detail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    return render(request, "order_detail.html", {
        "order": order,
        "stripe_public_key": os.getenv("STRIPE_PUBLIC_KEY")
    })


def create_order_checkout(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    line_items = []
    for item in order.items.all():
        line_item = {
            "price_data": {
                "currency": item.currency,
                "product_data": {"name": item.name},
                "unit_amount": int(item.price * 100),
                "tax_rates": [],
            },
            "quantity": 1,
        }

        if order.tax and order.tax.stripe_tax_rate_id:
            line_item["price_data"]["tax_rates"].append(order.tax.stripe_tax_rate_id)

        line_items.append(line_item)

    discounts = []
    if order.discount and order.discount.stripe_coupon_id:
        discounts.append({"coupon": order.discount.stripe_coupon_id})

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        discounts=discounts if discounts else None,
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
    )
    return JsonResponse({"id": session.id})


@csrf_exempt
def create_order_checkout(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    line_items = []
    for item in order.items.all():
        line_item = {
            "price_data": {
                "currency": item.currency,
                "product_data": {"name": item.name},
                "unit_amount": int(item.price * 100),
            },
            "quantity": 1,
        }

        if order.tax and order.tax.stripe_tax_rate_id:
            line_item["price_data"]["tax_behavior"] = "exclusive"
            line_item["tax_rates"] = [order.tax.stripe_tax_rate_id]

        line_items.append(line_item)

    discounts = []
    if order.discount and order.discount.stripe_coupon_id:
        discounts.append({"coupon": order.discount.stripe_coupon_id})

    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=line_items,
        mode="payment",
        discounts=discounts if discounts else None,
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
    )
    return JsonResponse({"id": session.id})


