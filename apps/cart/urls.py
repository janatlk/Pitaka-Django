from django.urls import path
from .views import (
    cart_view, add_to_cart, remove_from_cart, 
    update_quantity, clear_cart, cart_drawer
)

app_name = 'cart'

urlpatterns = [
    path('', cart_view, name='cart'),
    path('drawer/', cart_drawer, name='drawer'),
    path('add/<int:product_id>/', add_to_cart, name='add'),
    path('remove/<int:item_id>/', remove_from_cart, name='remove'),
    path('update/<int:item_id>/', update_quantity, name='update'),
    path('clear/', clear_cart, name='clear'),
]
