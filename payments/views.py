import stripe
from django.conf import settings
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404, render
from .models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY


def buy_item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': int(item.price * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://example.com/success',
            cancel_url='https://example.com/cancel',
        )
        return JsonResponse({'id': session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)})


def item_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    return render(request, 'item.html', {
        'item': item,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    })
