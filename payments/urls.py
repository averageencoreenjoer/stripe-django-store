from django.urls import path
from .views import item_detail, buy_item

urlpatterns = [
    path('item/<int:item_id>/', item_detail, name='item_detail'),
    path('buy/<int:item_id>/', buy_item, name='buy_item'),
]
