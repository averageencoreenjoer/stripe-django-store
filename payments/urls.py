from django.urls import path
from . import views

urlpatterns = [
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('create-payment-intent/<int:order_id>/', views.create_payment_intent, name='create_payment_intent'),
]
