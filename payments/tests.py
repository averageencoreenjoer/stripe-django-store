import pytest
from django.urls import reverse
from payments.models import Item, Order, Discount, Tax
from django.test import Client
from unittest.mock import patch


@pytest.mark.django_db
class TestStripeIntegration:

    def setup_method(self):
        self.client = Client()
        self.item = Item.objects.create(name='Test Item', description='Test Desc', price=100)
        self.discount = Discount.objects.create(name='Test Discount', percent=10)
        self.tax = Tax.objects.create(name='Test Tax', percent=20)
        self.order = Order.objects.create(discount=self.discount, tax=self.tax)
        self.order.items.add(self.item)

    def test_item_detail_page(self):
        url = reverse('item_detail', args=[self.item.id])
        response = self.client.get(url)
        assert response.status_code == 200
        assert 'Test Item' in response.content.decode()

    @patch('stripe.checkout.Session.create')
    def test_buy_item_creates_stripe_session(self, mock_create):
        mock_create.return_value.id = 'test_session_id'
        url = reverse('buy_item', args=[self.item.id])
        response = self.client.get(url)
        assert response.status_code == 200
        assert 'id' in response.json()
        mock_create.assert_called_once()

    def test_order_detail_page(self):
        url = reverse('order_detail', args=[self.order.id])
        response = self.client.get(url)
        assert response.status_code == 200
        assert 'Order #' in response.content.decode()

    @patch('stripe.checkout.Session.create')
    def test_create_order_checkout(self, mock_create):
        mock_create.return_value.id = 'test_session_id'
        url = reverse('create_payment_intent', args=[self.order.id])
        response = self.client.get(url)
        assert response.status_code == 200
        assert 'id' in response.json()
        mock_create.assert_called_once()

    def test_total_price_with_discount_and_tax(self):
        total = self.order.total_price()
        assert total == round(100 * 0.9 * 1.2, 2)

    def test_models_str_repr(self):
        assert str(self.item) == 'Test Item'
        assert str(self.discount) == 'Test Discount (10%)'
        assert str(self.tax) == 'Test Tax (20%)'
        assert str(self.order).startswith('Order #')
