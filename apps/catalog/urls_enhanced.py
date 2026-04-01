"""
SEO-Friendly URL Configuration for PITAKA Django
Supports clean URLs with proper slugs and hierarchical structure
"""

from django.urls import path, re_path
from django.views.generic import RedirectView
from .views import (
    catalog_view,
    product_detail_view,
    device_list_view,
    design_list_view,
    series_list_view,
    search_view,
    home_view,
)

app_name = 'catalog'

urlpatterns = [
    # Main catalog
    path('', catalog_view, name='catalog'),
    
    # Search
    path('search/', search_view, name='search'),
    
    # Device type listing (e.g., /iphone/, /samsung/)
    path('<slug:device_type>/', device_list_view, name='device_list'),
    
    # Device model listing (e.g., /iphone/iphone-17-pro-max/)
    path('<slug:device_type>/<slug:device_model>/', device_list_view, name='model_list'),
    
    # Design collection (e.g., /design/sunset/, /design/moonrise/)
    path('design/<slug:design_name>/', design_list_view, name='design_list'),
    
    # Series listing (e.g., /series/ultra-slim/, /series/proguard/)
    path('series/<slug:series>/', series_list_view, name='series_list'),
    
    # Product detail (e.g., /product/iphone-17-pro-max-sunset-ultra-slim/)
    path('product/<slug:slug>/', product_detail_view, name='product_detail'),
]
