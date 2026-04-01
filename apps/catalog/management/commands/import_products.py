"""
Management command to import PITAKA products from existing HTML structure
"""

from django.core.management.base import BaseCommand
from apps.catalog.models import Product, Category, Brand, ProductImage
from django.conf import settings
import os
import shutil
from pathlib import Path


class Command(BaseCommand):
    help = 'Импорт товаров PITAKA из существующей структуры'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--source',
            type=str,
            default='D:/ipitaka.finish',
            help='Путь к исходной папке с HTML файлами'
        )
        parser.add_argument(
            '--copy-images',
            action='store_true',
            help='Копировать изображения в media папку'
        )
    
    def handle(self, *args, **options):
        source_dir = Path(options['source'])
        copy_images = options['copy_images']
        
        self.stdout.write('Начинаем импорт товаров PITAKA...')
        self.stdout.write(f'Источник: {source_dir}')
        
        # Создаем категории
        self.stdout.write(self.style.SUCCESS('\nСоздание категорий...'))
        categories = self.create_categories()
        
        # Создаем бренд
        pitaka = self.create_brand()
        
        # Создаем товары
        products_data = self.get_all_products_data()
        
        created_count = 0
        updated_count = 0
        
        for product_data in products_data:
            created = self.create_or_update_product(
                product_data, 
                categories, 
                pitaka,
                source_dir,
                copy_images
            )
            if created:
                created_count += 1
            else:
                updated_count += 1
        
        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Импорт завершен!\n'
            f'   Создано товаров: {created_count}\n'
            f'   Обновлено товаров: {updated_count}'
        ))
    
    def create_categories(self):
        """Создать все категории"""
        cats_data = [
            {'name': 'Чехлы для iPhone', 'slug': 'iphone-cases'},
            {'name': 'Чехлы для Samsung', 'slug': 'samsung-cases'},
            {'name': 'Чехлы для Google Pixel', 'slug': 'pixel-cases'},
            {'name': 'Чехлы для iPad', 'slug': 'ipad-cases'},
            {'name': 'Чехлы для AirPods', 'slug': 'airpods-cases'},
            {'name': 'Ремешки для Apple Watch', 'slug': 'watch-bands'},
        ]
        
        categories = {}
        for cat_data in cats_data:
            cat, _ = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults={'name': cat_data['name']}
            )
            categories[cat_data['slug']] = cat
            self.stdout.write(f'  ✓ Категория: {cat.name}')
        
        return categories
    
    def create_brand(self):
        """Создать бренд PITAKA"""
        brand, _ = Brand.objects.get_or_create(
            slug='pitaka',
            defaults={'name': 'PITAKA'}
        )
        self.stdout.write(f'  ✓ Бренд: {brand.name}')
        return brand
    
    def get_all_products_data(self):
        """Получить все данные о товарах"""
        products = []
        
        # iPhone 17 Series
        iphone17_models = ['iPhone 17 Pro', 'iPhone 17 Pro Max']
        designs = ['Sunset', 'Moonrise', 'Amber', 'Indigo', 'Black/Grey Twill']
        for model in iphone17_models:
            for design in designs:
                products.append({
                    'model': model,
                    'design': design,
                    'series': 'ultra-slim',
                    'device_type': 'iphone',
                    'category': 'iphone-cases',
                    'price': 4990,
                })
        
        # iPhone 16 Series
        iphone16_models = ['iPhone 16 Pro', 'iPhone 16 Pro Max']
        for model in iphone16_models:
            for design in designs:
                products.append({
                    'model': model,
                    'design': design,
                    'series': 'ultra-slim',
                    'device_type': 'iphone',
                    'category': 'iphone-cases',
                    'price': 4490,
                })
        
        # iPhone Air
        for design in designs:
            products.append({
                'model': 'iPhone Air',
                'design': design,
                'series': 'ultra-slim',
                'device_type': 'iphone',
                'category': 'iphone-cases',
                'price': 4990,
            })
        
        # Samsung S26 Series
        samsung_s26_models = ['Galaxy S26 Ultra', 'Galaxy S26 Plus', 'Galaxy S26']
        for model in samsung_s26_models:
            for design in designs:
                products.append({
                    'model': model,
                    'design': design,
                    'series': 'ultra-slim',
                    'device_type': 'samsung',
                    'category': 'samsung-cases',
                    'price': 4990,
                })
        
        # Samsung S25 Series
        samsung_s25_models = ['Galaxy S25 Ultra', 'Galaxy S25 Plus', 'Galaxy S25']
        for model in samsung_s25_models:
            for design in designs:
                products.append({
                    'model': model,
                    'design': design,
                    'series': 'ultra-slim',
                    'device_type': 'samsung',
                    'category': 'samsung-cases',
                    'price': 4490,
                })
        
        # Samsung Fold/Flip
        fold_flip_models = ['Galaxy Z Fold7', 'Galaxy Z Flip7', 'Galaxy Z Fold6', 'Galaxy Z Flip6']
        for model in fold_flip_models:
            for design in ['Black/Grey Twill', 'Sunset', 'Moonrise']:
                products.append({
                    'model': model,
                    'design': design,
                    'series': 'ultra-slim',
                    'device_type': 'samsung',
                    'category': 'samsung-cases',
                    'price': 4990,
                })
        
        # AirPods
        airpods_models = ['AirPods Pro 3', 'AirPods Pro 2', 'AirPods Pro', 'AirPods 4']
        for model in airpods_models:
            for design in ['Sunset', 'Moonrise', 'Black/Grey Twill']:
                products.append({
                    'model': model,
                    'design': design,
                    'series': 'ultra-slim',
                    'device_type': 'airpods',
                    'category': 'airpods-cases',
                    'price': 2990,
                })
        
        # Apple Watch Bands
        for design in ['Modern', 'Moon', 'Mosaic', 'Stairs', 'Rhapsody']:
            products.append({
                'model': 'Apple Watch Ultra 2/Ultra',
                'design': design,
                'series': 'ultra-slim',
                'device_type': 'watch',
                'category': 'watch-bands',
                'price': 7990,
            })
        
        return products
    
    def create_or_update_product(self, product_data, categories, brand, source_dir, copy_images):
        """Создать или обновить товар"""
        from django.utils.text import slugify
        
        name = f"{product_data['model']} - {product_data['design']}"
        slug = slugify(f"{product_data['model']}-{product_data['design']}-{product_data['series']}")
        
        # Handle duplicate slugs
        base_slug = slug
        counter = 1
        while Product.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        category = categories.get(product_data['category'])
        
        product, created = Product.objects.update_or_create(
            slug=slug,
            defaults={
                'name': name,
                'category': category,
                'brand': brand,
                'device_type': product_data['device_type'],
                'device_model': product_data['model'],
                'design_name': product_data['design'],
                'series': product_data['series'],
                'price': product_data['price'],
                'description': f"Премиальный чехол {product_data['design']} для {product_data['model']}. Изготовлен из арамидного волокна.",
                'features': [
                    'Толщина 0.6 мм',
                    'Вес 8 грамм',
                    'Магнитное крепление MagSafe',
                    'Защита от царапин',
                    'Экологически чистые материалы'
                ],
                'is_new': product_data['model'] in ['iPhone 17 Pro', 'iPhone 17 Pro Max', 'iPhone Air', 'Galaxy S26 Ultra'],
                'is_featured': product_data['design'] in ['Sunset', 'Moonrise', 'Amber'],
            }
        )
        
        if created:
            self.stdout.write(f'  ✓ Создан: {product.name}')
        else:
            self.stdout.write(f'  ✓ Обновлен: {product.name}')
        
        return created
