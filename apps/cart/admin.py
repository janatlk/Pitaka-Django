from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'subtotal']
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['session_key', 'item_count', 'total_formatted', 'created_at', 'updated_at']
    list_filter = ['created_at']
    search_fields = ['session_key']
    inlines = [CartItemInline]
    readonly_fields = ['session_key', 'created_at', 'updated_at', 'get_whatsapp_url']
    
    fieldsets = (
        ('Информация', {
            'fields': ('session_key', 'created_at', 'updated_at')
        }),
        ('WhatsApp заказ', {
            'fields': ('get_whatsapp_url',)
        }),
    )
    
    def has_change_permission(self, request, obj=None):
        return False


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'subtotal_formatted']
    list_filter = ['cart']
