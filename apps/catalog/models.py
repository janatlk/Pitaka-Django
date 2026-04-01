from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """Категории товаров"""
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('Слаг', unique=True)
    image = models.ImageField('Изображение', upload_to='categories/', blank=True, null=True)
    description = models.TextField('Описание', blank=True)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Brand(models.Model):
    """Бренды"""
    name = models.CharField('Название', max_length=100)
    slug = models.SlugField('Слаг', unique=True)
    logo = models.ImageField('Логотип', upload_to='brands/', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Товары - чехлы и аксессуары"""
    
    DEVICE_CHOICES = [
        ('iphone', 'iPhone'),
        ('samsung', 'Samsung'),
        ('pixel', 'Google Pixel'),
        ('ipad', 'iPad'),
        ('airpods', 'AirPods'),
        ('watch', 'Apple Watch'),
    ]
    
    SERIES_CHOICES = [
        ('ultra-slim', 'Ultra-Slim'),
        ('proguard', 'ProGuard'),
        ('ultraguard', 'UltraGuard'),
    ]
    
    # Basic info
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('Слаг', unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Бренд')
    
    # Device compatibility
    device_type = models.CharField('Тип устройства', max_length=20, choices=DEVICE_CHOICES)
    device_model = models.CharField('Модель устройства', max_length=100)
    
    # Design
    design_name = models.CharField('Название дизайна', max_length=100)
    series = models.CharField('Серия', max_length=20, choices=SERIES_CHOICES)
    
    # Pricing
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    sale_price = models.DecimalField('Цена со скидкой', max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Stock & status
    stock = models.PositiveIntegerField('Остаток на складе', default=100)
    is_active = models.BooleanField('Активен', default=True)
    is_new = models.BooleanField('Новинка', default=False)
    is_featured = models.BooleanField('Хит продаж', default=False)
    
    # Content
    description = models.TextField('Описание', blank=True)
    features = models.JSONField('Особенности', default=list, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-is_featured', '-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['device_type', 'device_model']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['is_new']),
        ]
    
    def __str__(self):
        return f"{self.device_model} - {self.design_name}"

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('catalog:product_detail', kwargs={'slug': self.slug})

    @property
    def is_on_sale(self):
        return self.sale_price and self.sale_price < self.price
    
    def get_price_display(self):
        if self.is_on_sale:
            return f"{self.sale_price:,.0f} ₽"
        return f"{self.price:,.0f} ₽"
    
    def get_original_price_display(self):
        if self.is_on_sale:
            return f"{self.price:,.0f} ₽"
        return None
    
    @property
    def discount_percent(self):
        if self.is_on_sale:
            return int((1 - self.sale_price / self.price) * 100)
        return 0
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.device_model}-{self.design_name}-{self.series}")
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    """Изображения товаров"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', related_name='images')
    image = models.ImageField('Изображение', upload_to='products/')
    is_primary = models.BooleanField('Основное', default=False)
    order = models.PositiveIntegerField('Порядок', default=0)
    
    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'
        ordering = ['order', 'is_primary']
    
    def __str__(self):
        return f"Изображение для {self.product.name}"
    
    def save(self, *args, **kwargs):
        if self.is_primary:
            ProductImage.objects.filter(product=self.product).update(is_primary=False)
        super().save(*args, **kwargs)


class ProductVariant(models.Model):
    """Варианты товара (цвет, размер)"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', related_name='variants')
    name = models.CharField('Название', max_length=50)
    sku = models.CharField('Артикул', max_length=50, unique=True)
    price_adjustment = models.DecimalField('Наценка', max_digits=8, decimal_places=2, default=0)
    stock = models.PositiveIntegerField('Остаток', default=0)
    
    class Meta:
        verbose_name = 'Вариант'
        verbose_name_plural = 'Варианты'
    
    def __str__(self):
        return f"{self.product.name} - {self.name}"
