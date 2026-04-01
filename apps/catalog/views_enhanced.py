"""
Enhanced Views for PITAKA Django Migration
Includes SEO-optimized views, caching, and proper template rendering
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.db.models import Q, Count
from django.http import Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.catalog.models import Product, Category, Brand, ProductContent
from apps.cart.models import Cart
import json


@method_decorator(cache_page(60 * 15), name='dispatch')  # Cache for 15 minutes
class HomeView(TemplateView):
    """
    Enhanced Home Page with featured products, new arrivals, and collections
    """
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Best sellers (featured products)
        context['best_sellers'] = Product.objects.filter(
            is_active=True,
            is_featured=True
        ).select_related('category', 'brand').prefetch_related('images')[:8]
        
        # New arrivals
        context['new_arrivals'] = Product.objects.filter(
            is_active=True,
            is_new=True
        ).select_related('category', 'brand').prefetch_related('images')[:8]
        
        # Featured collections (designs)
        context['featured_designs'] = Product.objects.filter(
            is_active=True
        ).values('design_name').annotate(
            count=Count('id')
        ).order_by('-count')[:6]
        
        # Device types for navigation
        context['device_types'] = [
            {'slug': 'iphone', 'name': 'iPhone', 'icon': 'fa-mobile-screen'},
            {'slug': 'samsung', 'name': 'Samsung', 'icon': 'fa-mobile-screen-button'},
            {'slug': 'ipad', 'name': 'iPad', 'icon': 'fa-tablet-screen-button'},
            {'slug': 'watch', 'name': 'Apple Watch', 'icon': 'fa-watch'},
            {'slug': 'airpods', 'name': 'AirPods', 'icon': 'fa-headphones'},
        ]
        
        # Series comparison data
        context['series_list'] = [
            {'slug': 'ultra-slim', 'name': 'Ultra-Slim', 'tagline': 'Минимализм и лёгкость'},
            {'slug': 'proguard', 'name': 'ProGuard', 'tagline': 'Максимальная защита'},
            {'slug': 'ultraguard', 'name': 'UltraGuard', 'tagline': 'Баланс дизайна и прочности'},
        ]
        
        return context


@method_decorator(cache_page(60 * 10), name='dispatch')
class CatalogView(ListView):
    """
    Enhanced Catalog with advanced filtering and SEO
    """
    model = Product
    template_name = 'catalog/catalog.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).select_related(
            'category', 'brand'
        ).prefetch_related('images')
        
        # Filter by device type
        device_type = self.request.GET.get('device_type')
        if device_type:
            queryset = queryset.filter(device_type=device_type)
        
        # Filter by device model
        device_model = self.request.GET.get('device_model')
        if device_model:
            queryset = queryset.filter(device_model__icontains=device_model)
        
        # Filter by series
        series = self.request.GET.get('series')
        if series:
            queryset = queryset.filter(series=series)
        
        # Filter by design
        design = self.request.GET.get('design')
        if design:
            queryset = queryset.filter(design_name__icontains=design)
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Price range
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Search
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(device_model__icontains=query) |
                Q(design_name__icontains=query) |
                Q(slug__icontains=query)
            )
        
        # Ordering
        ordering = self.request.GET.get('order', '-is_featured')
        if ordering == 'price_asc':
            queryset = queryset.order_by('price')
        elif ordering == 'price_desc':
            queryset = queryset.order_by('-price')
        elif ordering == 'newest':
            queryset = queryset.order_by('-created_at')
        elif ordering == 'name':
            queryset = queryset.order_by('name')
        else:
            queryset = queryset.order_by('-is_featured', '-created_at')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # All categories for sidebar
        context['categories'] = Category.objects.all()
        
        # Filter options
        context['device_types'] = Product.objects.values_list(
            'device_type', flat=True
        ).distinct()
        
        context['device_models'] = Product.objects.filter(
            is_active=True
        ).values_list('device_model', flat=True).distinct()
        
        context['series_list'] = Product.objects.filter(
            is_active=True
        ).values_list('series', flat=True).distinct()
        
        context['designs'] = Product.objects.filter(
            is_active=True
        ).values_list('design_name', flat=True).distinct()
        
        # Active filters
        context['active_filters'] = {
            'device_type': self.request.GET.get('device_type'),
            'device_model': self.request.GET.get('device_model'),
            'series': self.request.GET.get('series'),
            'design': self.request.GET.get('design'),
            'category': self.request.GET.get('category'),
        }
        
        return context


class ProductDetailView(DetailView):
    """
    Enhanced Product Detail with SEO, related products, and WhatsApp integration
    """
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    
    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related(
            'category', 'brand'
        ).prefetch_related('images', 'media_files')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        
        # SEO metadata
        try:
            content = product.content
            context['meta_title'] = content.meta_title or f"{product.name} - PITAKA"
            context['meta_description'] = content.meta_description
            context['meta_keywords'] = content.meta_keywords
            context['faqs'] = content.faqs
            context['specs'] = content.specs
        except ProductContent.DoesNotExist:
            context['meta_title'] = f"{product.name} - PITAKA"
            context['meta_description'] = product.description[:160]
            context['faqs'] = []
            context['specs'] = {}
        
        # Related products (same category, exclude current)
        context['related_products'] = Product.objects.filter(
            category=product.category,
            is_active=True,
            device_model=product.device_model
        ).exclude(pk=product.pk).select_related('category')[:4]
        
        # Same design, different models
        context['same_design'] = Product.objects.filter(
            design_name=product.design_name,
            is_active=True
        ).exclude(pk=product.pk).select_related('category')[:4]
        
        # Add-on products (cross-sell)
        context['addon_products'] = product.addon_products.select_related(
            'add_on'
        ).prefetch_related('add_on__images')[:3]
        
        # Series comparison data
        context['series_comparison'] = [
            {
                'series': 'ultra-slim',
                'name': 'Ultra-Slim',
                'tagline': 'Минимализм и лёгкость',
                'weight': '≈20 г',
                'thickness': '≈0.99 мм',
                'protection': 'Базовая защита',
            },
            {
                'series': 'proguard',
                'name': 'ProGuard',
                'tagline': 'Максимальная защита',
                'weight': '≈35 г',
                'thickness': '≈2 мм',
                'protection': 'MIL-STD-810H · 2.44 м',
            },
            {
                'series': 'ultraguard',
                'name': 'UltraGuard',
                'tagline': 'Баланс дизайна и прочности',
                'weight': '≈35 г',
                'thickness': '≈2 мм',
                'protection': 'MIL-STD-810H · 1.22 м',
            },
        ]
        
        # WhatsApp share URL
        import urllib.parse
        message = f"Здравствуйте! Интересует товар: {product.name}\nЦена: {product.get_price_display()}"
        context['whatsapp_share_url'] = f"https://wa.me/{getattr(settings, 'WHATSAPP_PHONE', '79001234567')}?text={urllib.parse.quote(message)}"
        
        return context


class DeviceListView(ListView):
    """
    Device-specific listing (e.g., /iphone/, /samsung/)
    """
    model = Product
    template_name = 'catalog/device_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        device_type = self.kwargs.get('device_type')
        device_model = self.kwargs.get('device_model')
        
        queryset = Product.objects.filter(is_active=True).select_related(
            'category', 'brand'
        ).prefetch_related('images')
        
        if device_type:
            queryset = queryset.filter(device_type=device_type)
        if device_model:
            queryset = queryset.filter(device_model__icontains=device_model)
        
        return queryset.order_by('-is_featured', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        device_type = self.kwargs.get('device_type')
        device_model = self.kwargs.get('device_model')
        
        context['device_type'] = device_type
        context['device_model'] = device_model
        
        # Get all models for this device type
        if device_type:
            context['available_models'] = Product.objects.filter(
                device_type=device_type, is_active=True
            ).values_list('device_model', flat=True).distinct()
        
        return context


class DesignListView(ListView):
    """
    Design collection listing (e.g., /design/sunset/)
    """
    model = Product
    template_name = 'catalog/design_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        design_name = self.kwargs.get('design_name')
        return Product.objects.filter(
            is_active=True,
            design_name__icontains=design_name
        ).select_related('category', 'brand').prefetch_related('images')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['design_name'] = self.kwargs.get('design_name')
        return context


class SeriesListView(ListView):
    """
    Series-specific listing (e.g., /series/ultra-slim/)
    """
    model = Product
    template_name = 'catalog/series_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        series = self.kwargs.get('series')
        return Product.objects.filter(
            is_active=True,
            series=series
        ).select_related('category', 'brand').prefetch_related('images')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        series = self.kwargs.get('series')
        
        series_info = {
            'ultra-slim': {
                'name': 'Ultra-Slim',
                'description': 'Невероятно тонкий и лёгкий. Идеальный выбор для минималистов.',
                'image': 'series/ultra-slim.jpg',
            },
            'proguard': {
                'name': 'ProGuard',
                'description': 'Максимальная защита с арочной защитой углов.',
                'image': 'series/proguard.jpg',
            },
            'ultraguard': {
                'name': 'UltraGuard',
                'description': 'Баланс дизайна и прочности с цельным премиальным корпусом.',
                'image': 'series/ultraguard.jpg',
            },
        }
        
        context['series_info'] = series_info.get(series, {})
        context['series'] = series
        
        return context


class SearchView(ListView):
    """
    Enhanced search with suggestions
    """
    model = Product
    template_name = 'catalog/search.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        if not query:
            return Product.objects.none()
        
        return Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(device_model__icontains=query) |
            Q(design_name__icontains=query) |
            Q(slug__icontains=query) |
            Q(category__name__icontains=query)
        ).filter(is_active=True).select_related('category', 'brand')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        context['query'] = query
        
        # Search suggestions
        if query:
            context['suggestions'] = Product.objects.filter(
                Q(name__icontains=query) |
                Q(device_model__icontains=query) |
                Q(design_name__icontains=query)
            ).filter(is_active=True).values_list('name', flat=True)[:5]
        
        return context


# View functions for URL routing
home_view = HomeView.as_view()
catalog_view = CatalogView.as_view()
product_detail_view = ProductDetailView.as_view()
device_list_view = DeviceListView.as_view()
design_list_view = DesignListView.as_view()
series_list_view = SeriesListView.as_view()
search_view = SearchView.as_view()
