import os
import stripe
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Item, Order
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    }
    return render(request, 'order_detail.html', context)


@csrf_exempt
def create_payment_intent(request, order_id):
    if request.method != 'POST':
        return HttpResponseBadRequest('Only POST allowed')

    order = get_object_or_404(Order, id=order_id)
    amount = int(order.get_total() * 100)  # в центах
    currency = order.get_currency()

    try:
        payment_intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            automatic_payment_methods={'enabled': True},
            metadata={'order_id': order.id},
        )
        return JsonResponse({'clientSecret': payment_intent['client_secret']})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
