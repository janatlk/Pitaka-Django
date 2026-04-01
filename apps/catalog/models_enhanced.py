# ENHANCED MODELS FOR MIGRATION
# Add these fields to existing apps/catalog/models.py

from django.db import models
from django.utils.text import slugify


# === ADD TO EXISTING Product MODEL ===

class ProductContent(models.Model):
    """
    SEO and content data extracted from HTML pages
    One-to-one with Product
    """
    product = models.OneToOneField(
        'Product', 
        on_delete=models.CASCADE, 
        related_name='content'
    )
    
    # SEO Fields
    meta_title = models.CharField('Meta Title', max_length=200, blank=True)
    meta_description = models.TextField('Meta Description', blank=True)
    meta_keywords = models.CharField('Meta Keywords', max_length=500, blank=True)
    
    # Rich Content (from HTML sections)
    description_html = models.TextField('HTML Description', blank=True)
    features_list = models.JSONField('Features List', default=list)
    
    # Technical specs (from comparison section)
    specs = models.JSONField('Specifications', default=dict, blank=True)
    # Example: {"weight": "≈20 г", "thickness": "≈0.99 мм", "protection": "Базовая"}
    
    # FAQ Section
    faqs = models.JSONField('FAQs', default=list)
    # Example: [{"question": "...", "answer": "..."}, ...]
    
    class Meta:
        verbose_name = 'Контент товара'
        verbose_name_plural = 'Контенты товаров'


class ProductMedia(models.Model):
    """
    Enhanced media management with video support
    """
    product = models.ForeignKey(
        'Product', 
        on_delete=models.CASCADE, 
        related_name='media_files'
    )
    
    MEDIA_TYPE_CHOICES = [
        ('image', 'Изображение'),
        ('video', 'Видео'),
        ('model3d', '3D Модель'),
    ]
    
    media_type = models.CharField('Тип медиа', max_length=20, choices=MEDIA_TYPE_CHOICES, default='image')
    file = models.FileField('Файл', upload_to='products/media/')
    caption = models.CharField('Подпись', max_length=200, blank=True)
    is_primary = models.BooleanField('Основное', default=False)
    order = models.PositiveIntegerField('Порядок', default=0)
    
    class Meta:
        verbose_name = 'Медиа файл'
        verbose_name_plural = 'Медиа файлы'
        ordering = ['order', 'is_primary']


class DesignCollection(models.Model):
    """
    Design collections (Sunset, Moonrise, Indigo, Amber, etc.)
    Groups products by design across different device models
    """
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('Слаг', unique=True)
    description = models.TextField('Описание', blank=True)
    
    # Collection colors for UI
    color_hex = models.CharField('Цвет (HEX)', max_length=7, default='#000000')
    preview_image = models.ImageField('Превью', upload_to='collections/', blank=True)
    
    is_featured = models.BooleanField('Рекомендуем', default=False)
    
    class Meta:
        verbose_name = 'Коллекция дизайна'
        verbose_name_plural = 'Коллекции дизайнов'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


# === ADD TO EXISTING Product MODEL ===
# Add this field to link Product to DesignCollection
# design_collection = models.ForeignKey(
#     DesignCollection, 
#     on_delete=models.SET_NULL, 
#     null=True, 
#     blank=True,
#     verbose_name='Коллекция дизайна',
#     related_name='products'
# )


class CompatibleDevice(models.Model):
    """
    Many-to-Many relationship for device compatibility
    More flexible than single device_model field
    """
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='compatible_devices')
    device_type = models.CharField('Тип', max_length=20, choices=Product.DEVICE_CHOICES)
    device_model = models.CharField('Модель', max_length=100)
    is_primary = models.BooleanField('Основное', default=False)
    
    class Meta:
        verbose_name = 'Совместимое устройство'
        verbose_name_plural = 'Совместимые устройства'
        unique_together = ['product', 'device_model']


class SeriesComparison(models.Model):
    """
    Comparison data for series (Ultra-Slim vs ProGuard vs UltraGuard)
    """
    series = models.CharField('Серия', max_length=20, choices=Product.SERIES_CHOICES, unique=True)
    display_name = models.CharField('Отображаемое имя', max_length=50)
    tagline = models.CharField('Слоган', max_length=200, blank=True)
    
    # Comparison attributes
    weight = models.CharField('Вес', max_length=50, blank=True)
    thickness = models.CharField('Толщина', max_length=50, blank=True)
    protection_level = models.CharField('Уровень защиты', max_length=100, blank=True)
    
    # Features
    features = models.JSONField('Особенности', default=list)
    
    # Images for comparison table
    comparison_image = models.ImageField('Изображение для сравнения', upload_to='comparison/', blank=True)
    button_image = models.ImageField('Изображение кнопки', upload_to='comparison/', blank=True)
    protection_image = models.ImageField('Изображение защиты', upload_to='comparison/', blank=True)
    
    order = models.PositiveIntegerField('Порядок', default=0)
    
    class Meta:
        verbose_name = 'Сравнение серий'
        verbose_name_plural = 'Сравнения серий'
        ordering = ['order']


class AddOnProduct(models.Model):
    """
    Cross-sell products (MagEZ Grip, Wallet, Power Bank)
    Shown on product detail page as "Рекомендуем"
    """
    main_product = models.ForeignKey(
        'Product', 
        on_delete=models.CASCADE, 
        related_name='addon_products'
    )
    add_on = models.ForeignKey(
        'Product', 
        on_delete=models.CASCADE, 
        related_name='addon_for'
    )
    
    discount_price = models.DecimalField('Цена со скидкой', max_digits=10, decimal_places=2, null=True, blank=True)
    original_price = models.DecimalField('Оригинальная цена', max_digits=10, decimal_places=2, null=True, blank=True)
    order = models.PositiveIntegerField('Порядок', default=0)
    
    class Meta:
        verbose_name = 'Дополнительный товар'
        verbose_name_plural = 'Дополнительные товары'
        ordering = ['order']
        unique_together = ['main_product', 'add_on']
