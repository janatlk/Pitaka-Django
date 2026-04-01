from django.urls import path
from .views import catalog_view, product_detail_view, device_list_view, search_view

app_name = 'catalog'

urlpatterns = [
    path('', catalog_view, name='catalog'),
    path('search/', search_view, name='search'),
    path('product/<slug:slug>/', product_detail_view, name='product_detail'),
    path('<slug:device_type>/', device_list_view, name='device_list'),
    path('<slug:device_type>/<slug:device_model>/', device_list_view, name='model_list'),
]
