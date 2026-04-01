# Management command for importing products from HTML files
# Usage: python manage.py import_html_products [--dry-run]

import os
import sys
import re
from pathlib import Path
from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError
from django.utils.text import slugify

# Check if BeautifulSoup is available
try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None


class Command(BaseCommand):
    help = 'Import products from HTML files in pitaka_previous_files directory'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Run without creating products (preview mode)',
        )
        parser.add_argument(
            '--source-dir',
            type=str,
            default=None,
            help='Source directory with HTML files',
        )

    def handle(self, *args, **options):
        if BeautifulSoup is None:
            raise CommandError(
                'BeautifulSoup is not installed. Run: pip install beautifulsoup4'
            )

        from apps.catalog.models import Product, Category, Brand, ProductImage

        # Determine source directory
        if options['source_dir']:
            source_dir = Path(options['source_dir'])
        else:
            # Go up from apps/catalog/management/commands/ to project root, then to pitaka_previous_files
            source_dir = Path(__file__).resolve().parent.parent.parent.parent.parent / 'pitaka_previous_files' / 'ipitaka.finish' / 'pages'

        if not source_dir.exists():
            raise CommandError(f'Source directory not found: {source_dir}')

        dry_run = options['dry_run']

        self.stdout.write(self.style.SUCCESS(f'Source directory: {source_dir}'))
        self.stdout.write(self.style.WARNING(f'Mode: {"DRY RUN" if dry_run else "IMPORT"}'))
        self.stdout.write('')

        # Find all HTML files (exclude core pages)
        exclude_files = ['index.html', 'catalog.html', 'menu.html', 'account.html']
        html_files = [f for f in source_dir.glob('*.html') if f.name not in exclude_files]

        self.stdout.write(f'Found {len(html_files)} HTML files to process')
        self.stdout.write('')

        created_count = 0
        skipped_count = 0
        error_count = 0

        for html_file in sorted(html_files):
            try:
                result = self.process_html_file(html_file, dry_run)
                if result:
                    created_count += 1
                else:
                    skipped_count += 1
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ❌ Error: {e}'))
                error_count += 1

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS(f'Summary:'))
        self.stdout.write(self.style.SUCCESS(f'  Processed: {len(html_files)}'))
        self.stdout.write(self.style.SUCCESS(f'  Created: {created_count}'))
        self.stdout.write(self.style.SUCCESS(f'  Skipped: {skipped_count}'))
        self.stdout.write(self.style.SUCCESS(f'  Errors: {error_count}'))

        if dry_run:
            self.stdout.write(self.style.WARNING('\nThis was a DRY RUN. No products were created.'))
            self.stdout.write(self.style.WARNING('Run without --dry-run to import products.'))

    def process_html_file(self, filepath, dry_run=False):
        """Process a single HTML file and create product"""
        
        from apps.catalog.models import Product, Category, Brand, ProductImage

        self.stdout.write(f'Processing: {filepath.name}')

        # Parse HTML
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        soup = BeautifulSoup(content, 'html.parser')

        # Extract data
        data = self.extract_product_data(soup, filepath)

        if not data.get('device_model'):
            self.stdout.write(self.style.WARNING(f'  Skipping: No device model found'))
            return False

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
            self.stdout.write(self.style.SUCCESS(f'  [DRY RUN] Would create: {data["name"]}'))
            self.stdout.write(f'     Slug: {slug}')
            self.stdout.write(f'     Price: {data["price"]}')
            self.stdout.write(f'     Images: {len(data["images"])}')
            return True

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

        # Create product images (just store paths, don't validate)
        for i, img_src in enumerate(data['images'][:5]):
            img_name = os.path.basename(img_src)
            img_path = f'pitaka/images/webp/{img_name}'

            ProductImage.objects.create(
                product=product,
                image=img_path,
                is_primary=(i == 0),
                order=i
            )

        self.stdout.write(self.style.SUCCESS(f'  Created: {product.name}'))
        return True

    def extract_product_data(self, soup, filepath):
        """Extract product data from parsed HTML"""
        
        data = {
            'filename': filepath.stem,
            'name': None,
            'price': None,
            'device_type': 'iphone',
            'device_model': None,
            'design_name': None,
            'series': None,
            'images': [],
            'features': [],
            'specs': {},
            'faqs': [],
        }

        # Extract name
        name_el = soup.find('h1', id='productName')
        if name_el:
            data['name'] = name_el.get_text(strip=True)
        else:
            data['name'] = filepath.stem.replace('-', ' ').replace('_', ' ').title()

        # Extract price
        price_el = soup.find('span', id='price')
        if price_el:
            try:
                price_text = price_el.get_text(strip=True)
                data['price'] = Decimal(price_text.replace('$', ''))
            except:
                data['price'] = Decimal('4990')

        # Extract device model
        model_select = soup.find('select', id='model')
        if model_select:
            first_option = model_select.find('option')
            if first_option:
                data['device_model'] = first_option.get_text(strip=True)

        if not data['device_model']:
            # Infer from filename
            data['device_model'] = self.infer_device_model(filepath.stem)

        # Extract series
        category_el = soup.find('div', id='category')
        if category_el:
            series_text = category_el.get_text(strip=True).lower()
            if 'slim' in series_text or 'ultra' in series_text:
                data['series'] = 'ultra-slim'
            elif 'prog' in series_text or 'proguard' in series_text:
                data['series'] = 'proguard'
            elif 'ultrag' in series_text or 'ultraguard' in series_text:
                data['series'] = 'ultraguard'

        if not data['series']:
            data['series'] = 'ultra-slim'

        # Extract design name
        data['design_name'] = self.infer_design_name(filepath.stem)

        # Extract images
        main_image = soup.find('img', id='mainPhoto')
        if main_image and main_image.get('src'):
            data['images'].append(main_image['src'])

        thumbs = soup.select('.thumbs img')
        for thumb in thumbs:
            src = thumb.get('src')
            if src and src not in data['images']:
                data['images'].append(src)

        # Extract features
        sections = soup.select('.aramid-text p, .weave-text p, .thin-text p, .pitatap-text p')
        for section in sections:
            text = section.get_text(strip=True)
            if text and len(text) > 20:
                data['features'].append(text)

        # Extract specs
        spec_elements = soup.select('.thin-specs .spec')
        for spec in spec_elements:
            label = spec.find('span', class_='label')
            value = spec.find('span', class_='value')
            if label and value:
                label_text = label.get_text(strip=True).lower()
                value_text = value.get_text(strip=True)
                if 'толщина' in label_text:
                    data['specs']['thickness'] = value_text
                elif 'вес' in label_text:
                    data['specs']['weight'] = value_text

        # Extract FAQs
        faq_items = soup.select('.faq-item')
        for item in faq_items:
            question = item.find('div', class_='faq-question')
            answer = item.find('div', class_='faq-answer')
            if question and answer:
                data['faqs'].append({
                    'question': question.get_text(strip=True),
                    'answer': answer.get_text(strip=True)
                })

        # Determine device type
        filename_lower = filepath.stem.lower()
        if 'samsung' in filename_lower or 'galaxy' in filename_lower:
            data['device_type'] = 'samsung'
        elif 'ipad' in filename_lower:
            data['device_type'] = 'ipad'
        elif 'airpods' in filename_lower:
            data['device_type'] = 'airpods'
        elif 'watch' in filename_lower:
            data['device_type'] = 'watch'

        return data

    def infer_device_model(self, filename):
        """Infer device model from filename"""
        patterns = {
            r'iphone.*17.*pro.*max': 'iPhone 17 Pro Max',
            r'iphone.*17.*pro': 'iPhone 17 Pro',
            r'iphone.*17': 'iPhone 17',
            r'iphoneair': 'iPhone Air',
            r'iphone.*16.*pro.*max': 'iPhone 16 Pro Max',
            r'iphone.*16.*pro': 'iPhone 16 Pro',
            r'iphone.*16': 'iPhone 16',
            r'samsung.*s26.*ultra': 'Galaxy S26 Ultra',
            r'samsung.*s26.*plus': 'Galaxy S26 Plus',
            r'samsung.*s25.*ultra': 'Galaxy S25 Ultra',
            r'samsung.*s25.*plus': 'Galaxy S25 Plus',
            r'samsung.*fold7': 'Galaxy Z Fold7',
            r'samsung.*flip7': 'Galaxy Z Flip7',
            r'ipad.*pro.*13': 'iPad Pro 13"',
            r'ipad.*pro.*11': 'iPad Pro 11"',
            r'ipad.*air': 'iPad Air',
        }

        for pattern, model in patterns.items():
            if re.search(pattern, filename, re.IGNORECASE):
                return model

        return None

    def infer_design_name(self, filename):
        """Infer design name from filename"""
        patterns = {
            r'sunset': 'Sunset',
            r'moonrise': 'Moonrise',
            r'amber': 'Amber',
            r'indigo': 'Indigo',
            r'lucid': 'Lucid Blue',
            r'golden.*glint': 'Golden Glint',
            r'black.*twill': 'Black/Grey Twill',
            r'milky': 'Milky',
            r'over.*horizon': 'Over the Horizon',
            r'monogram': 'Monogram',
        }

        for pattern, design in patterns.items():
            if re.search(pattern, filename, re.IGNORECASE):
                return design

        return 'Black/Grey Twill'
