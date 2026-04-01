from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from apps.catalog.models import Product
from .models import Cart, CartItem


def get_or_create_cart(request):
    """Получить или создать корзину"""
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
    cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


@require_POST
def add_to_cart(request, product_id):
    """Добавить товар в корзину"""
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    cart = get_or_create_cart(request)
    
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    
    # Return JSON for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.item_count,
            'message': f'{product.name} добавлен в корзину'
        })
    
    messages.success(request, f'{product.name} добавлен в корзину')
    return redirect('cart:cart')


@require_POST
def remove_from_cart(request, item_id):
    """Удалить товар из корзины"""
    cart = get_or_create_cart(request)
    cart.items.filter(pk=item_id).delete()
    
    messages.success(request, 'Товар удален из корзины')
    return redirect('cart:cart')


@require_POST
def update_quantity(request, item_id):
    """Обновить количество товара"""
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        item.quantity = quantity
        item.save()
    else:
        item.delete()
    
    return redirect('cart:cart')


@require_POST
def clear_cart(request):
    """Очистить корзину"""
    cart = get_or_create_cart(request)
    cart.clear()
    
    messages.success(request, 'Корзина очищена')
    return redirect('catalog:catalog')


def cart_view(request):
    """Страница корзины"""
    cart = get_or_create_cart(request)
    whatsapp_url = cart.get_whatsapp_url()
    
    return render(request, 'cart/cart.html', {
        'cart': cart,
        'whatsapp_url': whatsapp_url
    })


def cart_drawer(request):
    """Cart drawer for AJAX"""
    cart = get_or_create_cart(request)
    return render(request, 'includes/cart_drawer.html', {
        'cart': cart
    })
