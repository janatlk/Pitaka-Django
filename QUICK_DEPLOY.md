# 🚀 Quick Deploy Guide

Choose your deployment platform:

---

## Option 1: Railway.app (Easiest - FREE)

**Time: 10 minutes**

### Steps:

1. **Push to GitHub**
   ```bash
   git remote add origin https://github.com/yourusername/pitaka-django.git
   git push -u origin main
   ```

2. **Connect Railway**
   - Go to https://railway.app
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Add Environment Variables**
   In Railway dashboard, add:
   ```
   SECRET_KEY=your-secret-key-here
   DEBUG=False
   ALLOWED_HOSTS=*.railway.app
   DB_ENGINE=django.db.backends.postgresql
   ```

4. **Add PostgreSQL**
   - Click "+ New"
   - Select "Database" → "PostgreSQL"
   - Railway auto-configures database variables

5. **Deploy**
   - Railway auto-deploys on push
   - Wait for build to complete
   - Click "Generate Domain" to get your URL

**Done!** Your site is live at `https://your-project.railway.app`

---

## Option 2: PythonAnywhere (FREE Tier)

**Time: 15 minutes**

### Steps:

1. **Sign Up**
   - Go to https://www.pythonanywhere.com
   - Create free account

2. **Upload Code**
   - Open Bash console
   - Clone your repo:
     ```bash
     git clone https://github.com/yourusername/pitaka-django.git
     cd pitaka-django
     ```

3. **Setup Virtual Environment**
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Configure Database**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

5. **Collect Static**
   ```bash
   python manage.py collectstatic --noinput
   ```

6. **Configure Web App**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Select "Manual configuration"
   - Python 3.10
   - Set paths:
     - Source code: `/home/yourusername/pitaka-django`
     - Working directory: `/home/yourusername/pitaka-django`
     - Virtualenv: `/home/yourusername/pitaka-django/venv`

7. **Configure WSGI**
   - Click on WSGI configuration file link
   - Uncomment and modify:
     ```python
     import os
     import sys
     path = '/home/yourusername/pitaka-django'
     if path not in sys.path:
         sys.path.append(path)
     os.environ['DJANGO_SETTINGS_MODULE'] = 'pitaka.settings'
     from django.core.wsgi import get_wsgi_application
     application = get_wsgi_application()
     ```

8. **Configure Static Files**
   - In "Web" tab, scroll to "Static files"
   - Add:
     - URL: `/static/`
     - Directory: `/home/yourusername/pitaka-django/staticfiles/`
   - Add:
     - URL: `/media/`
     - Directory: `/home/yourusername/pitaka-django/media/`

9. **Reload**
   - Click green "Reload" button

**Done!** Your site is live at `https://yourusername.pythonanywhere.com`

---

## Option 3: VPS (DigitalOcean Droplet - $5/month)

**Time: 30 minutes**

### Steps:

1. **Create Droplet**
   - Go to DigitalOcean
   - Create Droplet: Ubuntu 22.04
   - Size: Basic ($5/month)

2. **SSH into Server**
   ```bash
   ssh root@your-server-ip
   ```

3. **Install Dependencies**
   ```bash
   apt update
   apt install -y python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl
   ```

4. **Clone Repository**
   ```bash
   cd /var/www
   git clone https://github.com/yourusername/pitaka-django.git
   cd pitaka-django
   ```

5. **Setup Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install -r requirements.txt
   pip install gunicorn psycopg2-binary
   ```

6. **Configure PostgreSQL**
   ```bash
   sudo -u postgres psql
   CREATE DATABASE pitaka;
   CREATE USER pitaka_user WITH PASSWORD 'your-password';
   ALTER ROLE pitaka_user SET client_encoding TO 'utf8';
   ALTER ROLE pitaka_user SET default_transaction_isolation TO 'read committed';
   ALTER ROLE pitaka_user SET timezone TO 'UTC';
   GRANT ALL PRIVILEGES ON DATABASE pitaka TO pitaka_user;
   \q
   ```

7. **Create .env File**
   ```bash
   nano .env
   ```
   Add:
   ```
   SECRET_KEY=your-secret-key
   DEBUG=False
   ALLOWED_HOSTS=your-domain.com,www.your-domain.com,your-server-ip
   DB_ENGINE=django.db.backends.postgresql
   DB_NAME=pitaka
   DB_USER=pitaka_user
   DB_PASSWORD=your-password
   DB_HOST=localhost
   DB_PORT=5432
   ```

8. **Run Migrations**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic --noinput
   ```

9. **Create Gunicorn Service**
   ```bash
   nano /etc/systemd/system/pitaka.service
   ```
   Add:
   ```ini
   [Unit]
   Description=PITAKA Django Application
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/var/www/pitaka-django
   ExecStart=/var/www/pitaka-django/venv/bin/gunicorn --access-log - --workers 3 --bind unix:/var/www/pitaka-django/pitaka.sock pitaka.wsgi:application

   [Install]
   WantedBy=multi-user.target
   ```

   Enable and start:
   ```bash
   systemctl daemon-reload
   systemctl start pitaka
   systemctl enable pitaka
   ```

10. **Configure Nginx**
    ```bash
    nano /etc/nginx/sites-available/pitaka
    ```
    Add:
    ```nginx
    server {
        listen 80;
        server_name your-domain.com www.your-domain.com your-server-ip;

        location = /favicon.ico { access_log off; log_not_found off; }
        
        location /static/ {
            alias /var/www/pitaka-django/staticfiles/;
        }

        location /media/ {
            alias /var/www/pitaka-django/media/;
        }

        location / {
            include proxy_params;
            proxy_pass http://unix:/var/www/pitaka-django/pitaka.sock;
        }
    }
    ```

    Enable and test:
    ```bash
    ln -s /etc/nginx/sites-available/pitaka /etc/nginx/sites-enabled
    nginx -t
    systemctl restart nginx
    ```

11. **Setup Firewall**
    ```bash
    ufw allow 'Nginx Full'
    ufw allow 'OpenSSH'
    ufw enable
    ```

12. **Setup SSL (Let's Encrypt)**
    ```bash
    apt install certbot python3-certbot-nginx
    certbot --nginx -d your-domain.com -d www.your-domain.com
    ```

**Done!** Your site is live at `https://your-domain.com`

---

## Option 4: Docker (Any Platform)

**Time: 15 minutes**

### Local Testing:
```bash
docker-compose up --build
```
Visit: http://localhost:8000

### Deploy to Render.com:
1. Push to GitHub
2. Connect Render to GitHub
3. Select "Web Service"
4. Choose Docker runtime
5. Add environment variables
6. Deploy

### Deploy to Railway with Docker:
1. Push to GitHub
2. Connect Railway
3. Railway auto-detects Dockerfile
4. Add environment variables
5. Deploy

---

## 📋 Environment Variables Template

Copy this to your `.env` file:

```env
# Security
SECRET_KEY=your-super-secret-key-min-50-chars
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (PostgreSQL)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=pitaka
DB_USER=pitaka_user
DB_PASSWORD=your-secure-password
DB_HOST=localhost
DB_PORT=5432

# WhatsApp
WHATSAPP_PHONE=996999999999

# Email (Optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@pitaka.kg
```

---

## 🆘 Need Help?

- Check DEPLOYMENT.md for detailed guide
- Check DEPLOYMENT_CHECKLIST.md for complete checklist
- Check logs: `journalctl -u pitaka -f` (VPS)
- Railway logs: Check "Deployments" tab
- PythonAnywhere logs: Check "Errors" tab

---

**Good luck with your deployment! 🚀**
