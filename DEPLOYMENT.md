# PITAKA Django Deployment Guide

## 📋 Pre-Deployment Checklist

### 1. Environment Variables (.env)
Create a `.env` file in production with:

```env
# SECURITY
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (PostgreSQL recommended for production)
DATABASE_URL=postgresql://user:password@localhost:5432/pitaka

# WhatsApp
WHATSAPP_PHONE=996999999999

# Email (for notifications)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=your-password
```

### 2. Static Files
```bash
# Collect all static files
python manage.py collectstatic --noinput

# This will copy 1040+ files to staticfiles/
```

### 3. Database Migrations
```bash
# Apply all migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 4. Import Products (if needed)
```bash
# Import products from HTML files
python manage.py import_html_products
```

---

## 🚀 Deployment Options

### Option 1: Railway.app (Recommended - Free Tier)

1. **Connect GitHub Repository**
   - Push your code to GitHub
   - Connect Railway to your GitHub repo

2. **Add Environment Variables**
   ```
   SECRET_KEY=your-secret-key
   DEBUG=False
   ALLOWED_HOSTS=*.railway.app
   ```

3. **Build Command**
   ```bash
   pip install -r requirements.txt
   python manage.py collectstatic --noinput
   python manage.py migrate
   ```

4. **Start Command**
   ```bash
   gunicorn pitaka.wsgi:application
   ```

### Option 2: PythonAnywhere (Free Tier)

1. **Upload Code**
   - Upload via Git or FTP

2. **Configure Web App**
   - Python version: 3.10+
   - Framework: Django
   - Path to manage.py: /home/yourusername/pitaka.django/manage.py

3. **Static Files**
   ```bash
   python3.10 manage.py collectstatic
   ```

4. **WSGI Configuration**
   - Update WSGI file with your Django path

### Option 3: VPS (DigitalOcean, Linode, etc.)

#### Nginx + Gunicorn Setup

1. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl
   ```

2. **Create PostgreSQL Database**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE pitaka;
   CREATE USER pitaka_user WITH PASSWORD 'your_password';
   ALTER ROLE pitaka_user SET client_encoding TO 'utf8';
   ALTER ROLE pitaka_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE pitaka_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE pitaka TO pitaka_user;
   \q
   ```

3. **Install Gunicorn**
   ```bash
   pip install gunicorn psycopg2-binary
   ```

4. **Create Gunicorn Service** (`/etc/systemd/system/pitaka.service`)
   ```ini
   [Unit]
   Description=PITAKA Django Application
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/var/www/pitaka.django
   ExecStart=/usr/local/bin/gunicorn --access-log - --workers 3 --bind unix:/var/www/pitaka.django/pitaka.sock pitaka.wsgi:application

   [Install]
   WantedBy=multi-user.target
   ```

5. **Configure Nginx** (`/etc/nginx/sites-available/pitaka`)
   ```nginx
   server {
       listen 80;
       server_name yourdomain.com www.yourdomain.com;

       location = /favicon.ico { access_log off; log_not_found off; }
       
       location /static/ {
           alias /var/www/pitaka.django/staticfiles/;
       }

       location /media/ {
           alias /var/www/pitaka.django/media/;
       }

       location / {
           include proxy_params;
           proxy_pass http://unix:/var/www/pitaka.django/pitaka.sock;
       }
   }
   ```

6. **Enable and Start**
   ```bash
   sudo ln -s /etc/nginx/sites-available/pitaka /etc/nginx/sites-enabled
   sudo nginx -t
   sudo systemctl restart nginx
   sudo systemctl daemon-reload
   sudo systemctl start pitaka
   sudo systemctl enable pitaka
   ```

7. **SSL with Let's Encrypt**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
   ```

---

## 🔧 Production Settings

### Update settings.py for Production

```python
# Security Settings
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Security Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Add this
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Security Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Static Files with WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Install WhiteNoise for Static Files
```bash
pip install whitenoise
```

---

## 📊 Database Configuration

### Development (SQLite)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Production (PostgreSQL)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
```

---

## 🧪 Testing Before Deployment

```bash
# Run all tests
python manage.py test

# Check for issues
python manage.py check --deploy

# Test with production settings
python manage.py check --settings=pitaka.settings_production
```

---

## 📝 Post-Deployment Tasks

1. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

2. **Import Products**
   ```bash
   python manage.py import_html_products
   ```

3. **Test All Pages**
   - Homepage: https://yourdomain.com/
   - Catalog: https://yourdomain.com/catalog/
   - Product Detail: https://yourdomain.com/catalog/product/.../
   - Cart: https://yourdomain.com/cart/
   - Admin: https://yourdomain.com/admin/

4. **Set Up Monitoring**
   - Sentry for error tracking
   - Google Analytics for traffic
   - Uptime monitoring (UptimeRobot, Pingdom)

5. **Set Up Backups**
   - Database backups (daily)
   - Media files backups (daily)
   - Code backups (Git)

---

## 🆘 Troubleshooting

### Static Files Not Loading
```bash
# Check STATIC_ROOT
python manage.py collectstatic --noinput

# Check file permissions
sudo chown -R www-data:www-data /var/www/pitaka.django/staticfiles
```

### Database Errors
```bash
# Run migrations
python manage.py migrate

# Check database connection
python manage.py dbshell
```

### 500 Errors
```bash
# Check logs
sudo tail -f /var/log/nginx/error.log
sudo journalctl -u pitaka -f

# Enable DEBUG temporarily
DEBUG=True (in .env)
```

---

## 📞 Support

For issues or questions:
- Check Django documentation: https://docs.djangoproject.com/
- Railway support: https://railway.app/help
- PythonAnywhere support: https://help.pythonanywhere.com/

---

**Last Updated**: 2026-04-01
**Version**: 1.0
