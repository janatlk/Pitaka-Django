# 🚀 PITAKA Django Deployment Checklist

## ✅ Pre-Deployment

### 1. Environment Setup
- [ ] Create `.env` file with production values
- [ ] Generate new SECRET_KEY (50+ characters)
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS with your domain
- [ ] Set up PostgreSQL database credentials
- [ ] Configure WhatsApp phone number
- [ ] Set up email credentials (if using)

### 2. Database
- [ ] Choose database (PostgreSQL recommended)
- [ ] Create database and user
- [ ] Test database connection
- [ ] Run migrations: `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`

### 3. Static Files
- [ ] Run `python manage.py collectstatic --noinput`
- [ ] Verify 1040+ files collected
- [ ] Check STATIC_ROOT configuration
- [ ] Test static file serving

### 4. Media Files
- [ ] Create media directory
- [ ] Set proper permissions
- [ ] Configure MEDIA_ROOT and MEDIA_URL
- [ ] Set up cloud storage (optional: AWS S3, Cloudinary)

### 5. Security
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Set up SSL/HTTPS
- [ ] Configure security settings in settings_production.py
- [ ] Set SECURE_SSL_REDIRECT=True
- [ ] Set SESSION_COOKIE_SECURE=True
- [ ] Set CSRF_COOKIE_SECURE=True

---

## 🎯 Platform-Specific Deployment

### Railway.app
- [ ] Push code to GitHub
- [ ] Connect Railway to GitHub repo
- [ ] Add environment variables in Railway dashboard
- [ ] Set build command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
- [ ] Set start command: `gunicorn pitaka.wsgi:application`
- [ ] Add PostgreSQL plugin
- [ ] Deploy and test

### PythonAnywhere
- [ ] Upload code via Git or FTP
- [ ] Create virtual environment: `python3.10 -m venv venv`
- [ ] Install requirements: `pip install -r requirements.txt`
- [ ] Run migrations: `python manage.py migrate`
- [ ] Collect static: `python manage.py collectstatic --noinput`
- [ ] Configure Web tab in PythonAnywhere dashboard
- [ ] Set WSGI configuration file
- [ ] Configure static files mapping
- [ ] Reload web app

### VPS (DigitalOcean, Linode, etc.)
- [ ] SSH into server
- [ ] Install dependencies (Python, PostgreSQL, Nginx, Gunicorn)
- [ ] Clone repository
- [ ] Set up virtual environment
- [ ] Install Python requirements
- [ ] Configure PostgreSQL database
- [ ] Run migrations
- [ ] Collect static files
- [ ] Create Gunicorn systemd service
- [ ] Configure Nginx reverse proxy
- [ ] Set up SSL with Let's Encrypt
- [ ] Configure firewall (ufw)
- [ ] Test and reload services

### Docker (Railway, Render, etc.)
- [ ] Build Docker image: `docker build -t pitaka .`
- [ ] Test locally: `docker-compose up`
- [ ] Push to container registry
- [ ] Deploy to hosting platform
- [ ] Configure environment variables
- [ ] Set up persistent volumes for media

---

## 🧪 Testing

### Functionality Tests
- [ ] Homepage loads correctly
- [ ] Product listing pages work
- [ ] Product detail pages load
- [ ] Shopping cart adds/removes items
- [ ] WhatsApp ordering works
- [ ] Search functionality works
- [ ] User registration works
- [ ] User login/logout works
- [ ] Admin panel accessible

### Performance Tests
- [ ] Page load time < 3 seconds
- [ ] Images are optimized
- [ ] Static files are compressed
- [ ] Database queries are optimized
- [ ] No N+1 query issues

### Security Tests
- [ ] HTTPS is enforced
- [ ] CSRF protection is active
- [ ] SQL injection protection tested
- [ ] XSS protection tested
- [ ] Admin URL is protected

---

## 📊 Post-Deployment

### Monitoring
- [ ] Set up error tracking (Sentry)
- [ ] Set up uptime monitoring (UptimeRobot)
- [ ] Configure logging
- [ ] Set up database backups (daily)
- [ ] Set up media file backups (daily)

### SEO
- [ ] Submit sitemap to Google Search Console
- [ ] Set up Google Analytics
- [ ] Configure robots.txt
- [ ] Add meta tags to all pages
- [ ] Test with Google Mobile-Friendly Test

### Documentation
- [ ] Update README with deployment instructions
- [ ] Document environment variables
- [ ] Create runbook for common issues
- [ ] Document backup/restore procedure

---

## 🆘 Troubleshooting

### Common Issues

**Static files not loading:**
```bash
python manage.py collectstatic --noinput
sudo chown -R www-data:www-data /path/to/staticfiles
```

**Database connection error:**
```bash
# Check database is running
sudo systemctl status postgresql

# Test connection
psql -U username -d database_name
```

**500 Internal Server Error:**
```bash
# Check Gunicorn logs
sudo journalctl -u pitaka -f

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log

# Temporarily enable DEBUG
DEBUG=True (in .env)
```

**Permission denied:**
```bash
sudo chown -R www-data:www-data /var/www/pitaka.django
sudo chmod -R 755 /var/www/pitaka.django
```

---

## 📞 Support Resources

- Django Documentation: https://docs.djangoproject.com/
- Railway Docs: https://docs.railway.app/
- PythonAnywhere Docs: https://help.pythonanywhere.com/
- Django Deployment: https://docs.djangoproject.com/en/stable/howto/deployment/

---

**Last Updated**: 2026-04-01
**Version**: 1.0
