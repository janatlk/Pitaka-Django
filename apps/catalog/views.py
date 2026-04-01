from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Product, Category


class CatalogView(ListView):
    """Каталог товаров"""
    model = Product
    template_name = 'catalog/catalog.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        
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
        
        # Search
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(device_model__icontains=query) |
                Q(design_name__icontains=query)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['device_types'] = Product.objects.values_list('device_type', flat=True).distinct()
        context['device_models'] = Product.objects.values_list('device_model', flat=True).distinct()
        context['series_list'] = Product.objects.values_list('series', flat=True).distinct()
        context['designs'] = Product.objects.values_list('design_name', flat=True).distinct()
        return context


class ProductDetailView(DetailView):
    """Детальная страница товара"""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Related products (same category, exclude current)
        context['related_products'] = Product.objects.filter(
            category=self.object.category,
            is_active=True,
            device_model=self.object.device_model
        ).exclude(pk=self.object.pk)[:4]
        
        # Same design, different models
        context['same_design'] = Product.objects.filter(
            design_name=self.object.design_name,
            is_active=True
        ).exclude(pk=self.object.pk)[:4]
        
        return context


class DeviceListView(ListView):
    """Список товаров по устройству"""
    model = Product
    template_name = 'catalog/device_list.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        device_type = self.kwargs.get('device_type')
        device_model = self.kwargs.get('device_model')
        
        queryset = Product.objects.filter(is_active=True)
        
        if device_type:
            queryset = queryset.filter(device_type=device_type)
        if device_model:
            queryset = queryset.filter(device_model=device_model)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['device_type'] = self.kwargs.get('device_type')
        context['device_model'] = self.kwargs.get('device_model')
        return context


class SearchView(ListView):
    """Поиск товаров"""
    model = Product
    template_name = 'catalog/search.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return Product.objects.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query) |
                Q(device_model__icontains=query) |
                Q(design_name__icontains=query) |
                Q(slug__icontains=query)
            ).filter(is_active=True)
        return Product.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


catalog_view = CatalogView.as_view()
product_detail_view = ProductDetailView.as_view()
device_list_view = DeviceListView.as_view()
search_view = SearchView.as_view()
