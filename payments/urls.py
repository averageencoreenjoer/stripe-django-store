from django.urls import path
from .views import item_detail, buy_item, order_detail, create_order_checkout

urlpatterns = [
    path('item/<int:item_id>/', item_detail, name='item_detail'),
    path('buy/<int:item_id>/', buy_item, name='buy_item'),
    path("order/<int:order_id>/", order_detail, name="order_detail"),
    path("create-payment-intent/<int:order_id>/", create_order_checkout, name="create_payment_intent"),
]
