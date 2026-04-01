from django.shortcuts import render
from django.views.generic import TemplateView
from django.db import models
from apps.catalog.models import Product


# Device type configuration
DEVICE_TYPES_CONFIG = {
    'iphone': {'name': 'iPhone', 'icon': 'fa-mobile-screen'},
    'samsung': {'name': 'Samsung', 'icon': 'fa-mobile-screen-button'},
    'ipad': {'name': 'iPad', 'icon': 'fa-tablet-screen-button'},
    'airpods': {'name': 'AirPods', 'icon': 'fa-headphones'},
    'watch': {'name': 'Watch', 'icon': 'fa-clock'},
    'pixel': {'name': 'Pixel', 'icon': 'fa-mobile-screen'},
}


class HomeView(TemplateView):
    """Главная страница"""
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Best sellers
        context['best_sellers'] = Product.objects.filter(
            is_active=True,
            is_featured=True
        )[:8]

        # New arrivals
        context['new_arrivals'] = Product.objects.filter(
            is_active=True,
            is_new=True
        )[:8]

        # Get device types that have products
        active_device_types = Product.objects.filter(
            is_active=True
        ).values_list('device_type', flat=True).distinct()

        # Build device types list with config
        context['device_types'] = [
            {'slug': dtype, **DEVICE_TYPES_CONFIG.get(dtype, {'name': dtype.title(), 'icon': 'fa-mobile-screen'})}
            for dtype in active_device_types
        ]

        # Featured designs
        context['featured_designs'] = Product.objects.filter(
            is_active=True
        ).values('design_name').annotate(
            count=models.Count('id')
        ).order_by('-count')[:4]

        return context


home_view = HomeView.as_view()
