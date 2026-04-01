from django.contrib import admin
from .models import Category, Brand, Product, ProductImage, ProductVariant


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'is_primary', 'order']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'device_model', 'design_name', 'series', 
        'get_price_display', 'is_active', 'is_new', 'is_featured',
        'stock'
    ]
    list_filter = [
        'device_type', 'device_model', 'series', 
        'is_active', 'is_new', 'is_featured', 'category'
    ]
    search_fields = ['name', 'device_model', 'design_name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active', 'is_new', 'is_featured', 'stock']
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'category', 'brand')
        }),
        ('Совместимость', {
            'fields': ('device_type', 'device_model')
        }),
        ('Дизайн', {
            'fields': ('design_name', 'series')
        }),
        ('Цена и наличие', {
            'fields': ('price', 'sale_price', 'stock')
        }),
        ('Статус', {
            'fields': ('is_active', 'is_new', 'is_featured')
        }),
        ('Описание', {
            'fields': ('description', 'features')
        }),
    )


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ['product', 'name', 'sku', 'price_adjustment', 'stock']
    list_filter = ['product']
    search_fields = ['name', 'sku']
