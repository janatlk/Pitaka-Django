# PITAKA Django Migration - Quick Start Guide

## 🚀 Execute Migration in 5 Steps

### Step 1: Install Dependencies

```bash
cd D:\ipitaka.django
pip install beautifulsoup4
```

### Step 2: Create Enhanced Models

The enhanced models have been created in `apps/catalog/models_enhanced.py`.

**Action:** Copy the enhanced models to `apps/catalog/models.py` or run:

```bash
# Windows PowerShell
Get-Content apps\catalog\models_enhanced.py | Add-Content apps\catalog\models.py

# Or manually append the content from models_enhanced.py to models.py
```

Then create migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 3: Import Products from HTML

```bash
# First, do a dry run to see what will be imported
python manage.py import_html_products --dry-run

# If everything looks good, run the actual import
python manage.py import_html_products
```

Expected output:
```
Found 140 HTML files to process
Mode: IMPORT

Processing: iphone-16pro-blacktwill.html
  ✅ Created: 600D Black/Grey (Twill) (PitaTap™)
Processing: iphone-17pro-sunset.html
  ✅ Created: Sunset (PitaTap™)
...

Summary:
  Processed: 140
  Created: 140
  Skipped: 0
  Errors: 0
```

### Step 4: Create Superuser

```bash
python manage.py createsuperuser
```

Enter your credentials when prompted.

### Step 5: Run Development Server

```bash
python manage.py runserver
```

Open browser: http://127.0.0.1:8000/

---

## 📁 Files Created

| File | Purpose |
|------|---------|
| `apps/catalog/models_enhanced.py` | Enhanced models (ProductContent, DesignCollection, etc.) |
| `apps/catalog/views_enhanced.py` | Enhanced views with caching and SEO |
| `apps/catalog/urls_enhanced.py` | SEO-friendly URL patterns |
| `apps/catalog/management/commands/import_html_products.py` | Management command for HTML import |
| `parse_html_products.py` | Standalone parser script (alternative) |
| `templates/catalog/product_detail.html` | Product detail template |
| `templates/catalog/catalog.html` | Catalog listing template |
| `templates/core/home.html` | Home page template |
| `MIGRATION_PLAN.md` | Detailed migration documentation |
| `QUICK_START.md` | This file |

---

## 🔧 Verify Installation

### 1. Check Products in Database

```bash
python manage.py shell
```

```python
from apps.catalog.models import Product, Category, DesignCollection

# Count products
print(f"Products: {Product.objects.count()}")

# List first 5 products
for p in Product.objects.all()[:5]:
    print(f"  - {p.name} ({p.device_model}) - {p.price} ₽")

# Check categories
for cat in Category.objects.all():
    print(f"Category: {cat.name} - {cat.products.count()} products")
```

### 2. Test URLs

Visit these URLs in your browser:

- Home: http://127.0.0.1:8000/
- Catalog: http://127.0.0.1:8000/catalog/
- iPhone: http://127.0.0.1:8000/catalog/iphone/
- Samsung: http://127.0.0.1:8000/catalog/samsung/
- Product: http://127.0.0.1:8000/catalog/product/iphone-17-pro-max-sunset-ultra-slim/
- Search: http://127.0.0.1:8000/catalog/search/?q=sunset
- Admin: http://127.0.0.1:8000/admin/

---

## 🎨 Next Steps After Migration

### 1. Copy Images to Media Folder

The HTML files reference images in `pitaka_previous_files/ipitaka.finish/images/`.

Copy them to the Django media folder:

```bash
# Windows (PowerShell)
Copy-Item -Path "pitaka_previous_files\ipitaka.finish\images" -Destination "media\pitaka\images" -Recurse

# Or use the provided script
python copy_images_to_media.py
```

### 2. Update Image Paths (if needed)

If images don't show up, update the `MEDIA_PREFIX` in the import command:

```python
# In apps/catalog/management/commands/import_html_products.py
# Change this line:
img_path = f'pitaka/images/webp/{img_name}'
# To match your actual media structure
```

### 3. Add Product Content Manually

For products that need additional SEO content:

1. Go to Admin: http://127.0.0.1:8000/admin/
2. Navigate to "Контенты товаров" (Product Content)
3. Add meta descriptions, keywords, and additional FAQs

### 4. Configure WhatsApp Number

Edit `.env` file:

```env
WHATSAPP_PHONE=996500770777
```

---

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'bs4'"

**Solution:**
```bash
pip install beautifulsoup4
```

### Issue: "No products found after import"

**Solution:**
1. Check if import command ran successfully
2. Verify source directory exists
3. Check Django shell: `Product.objects.count()`

### Issue: "Images not displaying"

**Solution:**
1. Ensure images are copied to `media/` folder
2. Check `MEDIA_URL` and `MEDIA_ROOT` in settings.py
3. Verify image paths in database match actual file locations

### Issue: "Template not found"

**Solution:**
1. Check `TEMPLATES` setting in settings.py
2. Ensure templates are in `templates/` directory
3. Run: `python manage.py collectstatic --noinput`

---

## 📊 Data Structure Reference

### Product Fields

| Field | Type | Example |
|-------|------|---------|
| name | CharField | "iPhone 17 Pro - Sunset (PitaTap™)" |
| slug | SlugField | "iphone-17-pro-sunset-pitatap" |
| device_type | ChoiceField | "iphone", "samsung", "ipad" |
| device_model | CharField | "iPhone 17 Pro" |
| design_name | CharField | "Sunset", "Moonrise", "Black" |
| series | ChoiceField | "ultra-slim", "proguard", "ultraguard" |
| price | DecimalField | 4990.00 |
| sale_price | DecimalField | 4490.00 (optional) |
| stock | PositiveIntegerField | 100 |
| is_active | BooleanField | True |
| is_new | BooleanField | True (for new arrivals) |
| is_featured | BooleanField | True (for best sellers) |

### URL Patterns

```
/                              → Home page
/catalog/                      → All products
/catalog/?series=ultra-slim    → Filter by series
/catalog/iphone/               → iPhone products
/catalog/iphone/iphone-17-pro/ → Specific model
/catalog/design/sunset/        → Sunset collection
/catalog/series/ultra-slim/    → Ultra-Slim series
/catalog/search/?q=moonrise    → Search
/catalog/product/<slug>/       → Product detail
/cart/                         → Shopping cart
/accounts/login/               → Login
/accounts/profile/             → User profile
/admin/                        → Django admin
```

---

## 📝 Useful Admin Operations

### 1. Mark Products as Featured

```bash
python manage.py shell
```

```python
from apps.catalog.models import Product

# Mark all Sunset products as featured
Product.objects.filter(design_name='Sunset').update(is_featured=True)

# Mark all new iPhone 17 products as new
Product.objects.filter(
    device_model__icontains='iPhone 17',
    is_active=True
).update(is_new=True)
```

### 2. Set Sale Prices

```python
from decimal import Decimal

# Apply 10% discount to all products
for product in Product.objects.filter(is_active=True):
    product.sale_price = product.price * Decimal('0.9')
    product.save()
```

### 3. Bulk Update Stock

```python
# Set stock for all products
Product.objects.update(stock=50)
```

---

## 🎯 Performance Optimization

### Enable Database-Level Pagination

Already implemented in views. Adjust items per page:

```python
# In apps/catalog/views.py
class CatalogView(ListView):
    paginate_by = 24  # Change from 12 to 24
```

### Add Database Indexes

Already defined in models.py:

```python
class Meta:
    indexes = [
        models.Index(fields=['slug']),
        models.Index(fields=['device_type', 'device_model']),
        models.Index(fields=['is_featured']),
        models.Index(fields=['is_new']),
    ]
```

### Enable Template Caching

Add to settings.py:

```python
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'TIMEOUT': 300,  # 5 minutes
    }
}
```

---

## 📞 Support Commands

### Export Products to CSV

```bash
python manage.py shell
```

```python
import csv
from apps.catalog.models import Product

with open('products_export.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Name', 'Device Model', 'Design', 'Series', 'Price', 'Stock'])
    
    for p in Product.objects.all():
        writer.writerow([p.name, p.device_model, p.design_name, p.series, p.price, p.stock])

print("Exported to products_export.csv")
```

### Generate Sitemap

```python
# Create apps/catalog/sitemap.py
from django.contrib.sitemaps import Sitemap
from .models import Product

class ProductSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    
    def items(self):
        return Product.objects.filter(is_active=True)
    
    def lastmod(self, obj):
        return obj.updated_at
```

---

## ✅ Migration Checklist

- [ ] Dependencies installed (beautifulsoup4)
- [ ] Enhanced models added to models.py
- [ ] Migrations created and applied
- [ ] Products imported from HTML
- [ ] Images copied to media folder
- [ ] Superuser created
- [ ] Server running without errors
- [ ] Home page displays products
- [ ] Product detail pages work
- [ ] Cart functionality works
- [ ] WhatsApp checkout tested
- [ ] Admin panel accessible
- [ ] Mobile responsive tested
- [ ] SEO meta tags present

---

**Last Updated:** 2026-04-01  
**Version:** 1.0
