from django.db import models
from django.conf import settings
import urllib.parse


class Cart(models.Model):
    """Корзина покупок"""
    session_key = models.CharField('Ключ сессии', max_length=100, unique=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
    
    def __str__(self):
        return f"Корзина {self.session_key}"
    
    @property
    def items_list(self):
        return self.items.all()
    
    @property
    def total(self):
        return sum(item.subtotal for item in self.items_list)
    
    @property
    def item_count(self):
        return sum(item.quantity for item in self.items_list)
    
    @property
    def total_formatted(self):
        return f"{self.total:,.0f} ₽"
    
    def get_whatsapp_message(self):
        """Генерация сообщения для WhatsApp"""
        lines = ["Здравствуйте! Хочу заказать:\n"]
        
        for item in self.items_list:
            product = item.product
            lines.append(f"- {product.device_model} ({product.design_name}) - {item.quantity} шт. — {item.subtotal:,.0f} ₽")
        
        lines.append(f"\nИтого: {self.total:,.0f} ₽")
        
        return "\n".join(lines)
    
    def get_whatsapp_url(self):
        """Генерация ссылки для WhatsApp"""
        message = self.get_whatsapp_message()
        encoded = urllib.parse.quote(message)
        phone = getattr(settings, 'WHATSAPP_PHONE', '79001234567')
        return f"https://wa.me/{phone}?text={encoded}"
    
    def clear(self):
        """Очистить корзину"""
        self.items.all().delete()


class CartItem(models.Model):
    """Элемент корзины"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина', related_name='items')
    product = models.ForeignKey('catalog.Product', on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField('Количество', default=1)
    added_at = models.DateTimeField('Дата добавления', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'
        unique_together = ['cart', 'product']
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    @property
    def subtotal(self):
        price = self.product.sale_price or self.product.price
        return float(price) * self.quantity
    
    @property
    def subtotal_formatted(self):
        return f"{self.subtotal:,.0f} ₽"
