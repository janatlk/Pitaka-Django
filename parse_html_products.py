#!/usr/bin/env python
"""
HTML Product Parser for PITAKA Migration
Extracts product data from 144 static HTML files and imports into Django database.

Usage:
    python parse_html_products.py [--dry-run] [--source-dir PATH]
"""

import os
import re
import sys
import json
from pathlib import Path
from bs4 import BeautifulSoup
from decimal import Decimal

# Django setup
BASE_DIR = Path(r'D:\ipitaka.django')
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pitaka.settings')

import django
django.setup()

from apps.catalog.models import Product, Category, Brand, ProductImage, ProductContent
from django.utils.text import slugify


# === CONFIGURATION ===
SOURCE_DIR = BASE_DIR / 'pitaka_previous_files' / 'ipitaka.finish' / 'pages'
MEDIA_PREFIX = 'pitaka/images/webp/'  # Adjust based on your media structure


# === PARSING PATTERNS ===

# Device model mapping from HTML filenames
DEVICE_MODEL_PATTERNS = {
    # iPhone patterns
    r'iphone-17pro': 'iPhone 17 Pro',
    r'iphone-17promax': 'iPhone 17 Pro Max',
    r'iphone-17': 'iPhone 17',
    r'iphoneair': 'iPhone Air',
    r'iphone-16pro': 'iPhone 16 Pro',
    r'iphone-16promax': 'iPhone 16 Pro Max',
    r'iphone-16': 'iPhone 16',
    r'iphone17pro': 'iPhone 17 Pro',
    r'iphone17promax': 'iPhone 17 Pro Max',
    r'iphone17': 'iPhone 17',
    r'iphoneair': 'iPhone Air',
    r'iphone16pro': 'iPhone 16 Pro',
    r'iphone16promax': 'iPhone 16 Pro Max',
    
    # Samsung patterns
    r'samsung-s26-ultra': 'Galaxy S26 Ultra',
    r'samsung-s26-plus': 'Galaxy S26 Plus',
    r'samsung-s25-ultra': 'Galaxy S25 Ultra',
    r'samsung-s25-plus': 'Galaxy S25 Plus',
    r'samsung-s25': 'Galaxy S25',
    r'samsung-galaxy-z-fold7': 'Galaxy Z Fold7',
    r'samsung-galaxy-z-flip7': 'Galaxy Z Flip7',
    
    # iPad patterns
    r'ipad-pro-13-m5': 'iPad Pro 13" (M5)',
    r'ipad-pro-11-m5': 'iPad Pro 11" (M5)',
    r'ipad-air-13': 'iPad Air 13"',
    r'ipad-air-11': 'iPad Air 11"',
}

# Design name patterns
DESIGN_PATTERNS = {
    r'sunset': 'Sunset',
    r'moonrise': 'Moonrise',
    r'amber': 'Amber',
    r'indigo': 'Indigo',
    r'lucid': 'Lucid Blue',
    r'golden.glint': 'Golden Glint',
    r'black.*twill': 'Black/Grey Twill',
    r'black': 'Black',
    r'milky': 'Milky',
    r'over.*horizon': 'Over the Horizon',
    r'monogram': 'Monogram',
}

# Series patterns
SERIES_PATTERNS = {
    r'uslim|ultra-slim|slim': 'ultra-slim',
    r'prog|proguard': 'proguard',
    r'ultrag|ultraguard': 'ultraguard',
}


def parse_html_file(filepath):
    """
    Parse a single HTML file and extract product data.
    Returns a dictionary with extracted data.
    """
    print(f"  Parsing: {filepath.name}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    data = {
        'filename': filepath.stem,
        'name': None,
        'price': None,
        'device_type': 'iphone',  # default
        'device_model': None,
        'design_name': None,
        'series': None,
        'images': [],
        'description': '',
        'features': [],
        'specs': {},
        'faqs': [],
    }
    
    # === Extract Product Name ===
    name_el = soup.find('h1', id='productName')
    if name_el:
        data['name'] = name_el.get_text(strip=True)
    else:
        # Try to infer from filename
        data['name'] = filepath.stem.replace('-', ' ').replace('_', ' ').title()
    
    # === Extract Price ===
    price_el = soup.find('span', id='price')
    if price_el:
        try:
            price_text = price_el.get_text(strip=True)
            data['price'] = Decimal(price_text.replace('$', ''))
        except:
            data['price'] = Decimal('4990')  # Default price
    
    # === Extract Device Model ===
    model_select = soup.find('select', id='model')
    if model_select:
        first_option = model_select.find('option')
        if first_option:
            data['device_model'] = first_option.get_text(strip=True)
    
    if not data['device_model']:
        # Infer from filename
        for pattern, model in DEVICE_MODEL_PATTERNS.items():
            if re.search(pattern, filepath.stem, re.IGNORECASE):
                data['device_model'] = model
                break
    
    # === Extract Series ===
    category_el = soup.find('div', id='category')
    if category_el:
        series_text = category_el.get_text(strip=True).lower()
        for pattern, series in SERIES_PATTERNS.items():
            if re.search(pattern, series_text, re.IGNORECASE):
                data['series'] = series
                break
    
    if not data['series']:
        # Default to ultra-slim
        data['series'] = 'ultra-slim'
    
    # === Extract Design Name ===
    for pattern, design in DESIGN_PATTERNS.items():
        if re.search(pattern, filepath.stem, re.IGNORECASE):
            data['design_name'] = design
            break
    
    if not data['design_name']:
        data['design_name'] = 'Black/Grey Twill'  # Default
    
    # === Extract Images ===
    main_image = soup.find('img', id='mainPhoto')
    if main_image and main_image.get('src'):
        data['images'].append(main_image['src'])
    
    # Get thumbnail images
    thumbs = soup.select('.thumbs img')
    for thumb in thumbs:
        src = thumb.get('src')
        if src and src not in data['images']:
            data['images'].append(src)
    
    # Get comparison images
    comparison_imgs = soup.select('.comparison img')
    for img in comparison_imgs[:3]:  # Limit to 3
        src = img.get('src')
        if src:
            data['images'].append(src)
    
    # === Extract Features (from sections) ===
    sections = soup.select('.aramid-text p, .weave-text p, .thin-text p, .pitatap-text p')
    for section in sections:
        text = section.get_text(strip=True)
        if text and len(text) > 20:
            data['features'].append(text)
    
    # === Extract Specs ===
    specs = {}
    spec_elements = soup.select('.thin-specs .spec')
    for spec in spec_elements:
        label = spec.find('span', class_='label')
        value = spec.find('span', class_='value')
        if label and value:
            label_text = label.get_text(strip=True).lower()
            value_text = value.get_text(strip=True)
            if 'толщина' in label_text or 'thickness' in label_text.lower():
                specs['thickness'] = value_text
            elif 'вес' in label_text or 'weight' in label_text.lower():
                specs['weight'] = value_text
    
    data['specs'] = specs
    
    # === Extract FAQs ===
    faq_items = soup.select('.faq-item')
    for item in faq_items:
        question = item.find('div', class_='faq-question')
        answer = item.find('div', class_='faq-answer')
        if question and answer:
            data['faqs'].append({
                'question': question.get_text(strip=True),
                'answer': answer.get_text(strip=True)
            })
    
    # === Determine Device Type ===
    filename_lower = filepath.stem.lower()
    if 'samsung' in filename_lower or 'galaxy' in filename_lower:
        data['device_type'] = 'samsung'
    elif 'ipad' in filename_lower:
        data['device_type'] = 'ipad'
    elif 'airpods' in filename_lower:
        data['device_type'] = 'airpods'
    elif 'watch' in filename_lower:
        data['device_type'] = 'watch'
    else:
        data['device_type'] = 'iphone'
    
    return data


def create_product_from_data(data, dry_run=False):
    """
    Create Django Product instance from parsed data.
    """
    if not data['device_model']:
        print(f"    ⚠️  Skipping: No device model found")
        return None
    
    # Get or create category
    category, _ = Category.objects.get_or_create(
        slug=data['device_type'],
        defaults={'name': data['device_type'].title()}
    )
    
    # Get or create brand
    brand, _ = Brand.objects.get_or_create(
        slug='pitaka',
        defaults={'name': 'PITAKA'}
    )
    
    # Create slug
    base_slug = slugify(f"{data['device_model']}-{data['design_name']}-{data['series']}")
    slug = base_slug
    counter = 1
    while Product.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    
    if dry_run:
        print(f"    📋 [DRY RUN] Would create: {data['name']}")
        print(f"       Slug: {slug}")
        print(f"       Price: {data['price']}")
        print(f"       Images: {len(data['images'])}")
        return None
    
    # Create product
    product = Product.objects.create(
        name=data['name'],
        slug=slug,
        category=category,
        brand=brand,
        device_type=data['device_type'],
        device_model=data['device_model'],
        design_name=data['design_name'],
        series=data['series'],
        price=data['price'] or Decimal('4990'),
        description='\n'.join(data['features'][:3]) if data['features'] else '',
        features=data['features'],
        is_active=True,
    )
    
    # Create product content (SEO, FAQs, specs)
    ProductContent.objects.create(
        product=product,
        meta_title=f"{data['name']} - PITAKA",
        meta_description=f"Купить {data['name']} из арамидного волокна. "
                        f"Серия: {data['series']}. "
                        f"Для {data['device_model']}.",
        specs=data['specs'],
        faqs=data['faqs'][:10],  # Limit to 10 FAQs
    )
    
    # Create product images
    for i, img_src in enumerate(data['images'][:5]):  # Limit to 5 images
        # Clean up image path
        img_name = os.path.basename(img_src)
        img_path = f"{MEDIA_PREFIX}{img_name}"
        
        # Check if file exists
        full_path = BASE_DIR / 'media' / MEDIA_PREFIX / img_name
        if full_path.exists():
            ProductImage.objects.create(
                product=product,
                image=img_path,
                is_primary=(i == 0),
                order=i
            )
        else:
            # Store as placeholder path
            ProductImage.objects.create(
                product=product,
                image=img_path,
                is_primary=(i == 0),
                order=i
            )
    
    print(f"    ✅ Created: {product.name}")
    return product


def main():
    """
    Main function to parse all HTML files and import products.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Parse HTML products and import to Django')
    parser.add_argument('--dry-run', action='store_true', help='Run without creating products')
    parser.add_argument('--source-dir', type=str, default=str(SOURCE_DIR), help='Source directory')
    args = parser.parse_args()
    
    source_path = Path(args.source_dir)
    
    if not source_path.exists():
        print(f"❌ Source directory not found: {source_path}")
        return
    
    # Find all HTML files
    html_files = list(source_path.glob('*.html'))
    # Exclude non-product pages
    exclude_files = ['index.html', 'catalog.html', 'menu.html', 'account.html']
    html_files = [f for f in html_files if f.name not in exclude_files]
    
    print(f"📁 Found {len(html_files)} HTML files to parse")
    print(f"📂 Source: {source_path}")
    print(f"{'🔍 DRY RUN' if args.dry_run else '🚀 IMPORTING'}\n")
    
    created_count = 0
    skipped_count = 0
    
    for html_file in sorted(html_files):
        try:
            data = parse_html_file(html_file)
            result = create_product_from_data(data, dry_run=args.dry_run)
            if result:
                created_count += 1
            else:
                skipped_count += 1
        except Exception as e:
            print(f"    ❌ Error parsing {html_file.name}: {e}")
            skipped_count += 1
    
    print(f"\n{'='*50}")
    print(f"📊 Summary:")
    print(f"   Processed: {len(html_files)}")
    print(f"   Created: {created_count}")
    print(f"   Skipped: {skipped_count}")
    if args.dry_run:
        print(f"\n⚠️  This was a DRY RUN. No products were created.")
        print(f"   Run without --dry-run to import products.")


if __name__ == '__main__':
    main()
