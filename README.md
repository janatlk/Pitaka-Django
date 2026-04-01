# PITAKA Django E-Commerce Site

Динамический интернет-магазин премиальных аксессуаров PITAKA на Django.

## 🚀 Быстрый старт

### Для Windows

1. **Запустите скрипт установки:**
   ```
   setup.bat
   ```

2. **Запустите сервер:**
   ```
   run.bat
   ```

3. **Откройте браузер:**
   ```
   http://127.0.0.1:8000
   ```

### Для macOS/Linux

1. **Запустите скрипт установки:**
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Запустите сервер:**
   ```bash
   source venv/bin/activate
   python manage.py runserver
   ```

3. **Откройте браузер:**
   ```
   http://127.0.0.1:8000
   ```

## 📦 Установка вручную

### 1. Установите Python

Скачайте с [python.org](https://www.python.org/downloads/)

### 2. Установите зависимости

```bash
pip install -r requirements.txt
```

### 3. Настройте переменные окружения

Скопируйте `.env.example` в `.env` и отредактируйте:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
WHATSAPP_PHONE=79001234567  # Ваш номер WhatsApp
```

### 4. Создайте миграции

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Создайте суперпользователя

```bash
python manage.py createsuperuser
```

### 6. Импортируйте товары

```bash
python manage.py import_products
```

### 7. Запустите сервер

```bash
python manage.py runserver
```

## 📁 Структура проекта

```
D:\ipitaka.django\
├── manage.py              # Django management script
├── requirements.txt       # Python зависимости
├── setup.bat             # Скрипт установки (Windows)
├── run.bat               # Запуск сервера (Windows)
├── .env                  # Переменные окружения
│
├── pitaka/               # Настройки Django
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── apps/                 # Приложения Django
│   ├── core/            # Главная страница
│   ├── catalog/         # Каталог товаров
│   ├── cart/            # Корзина (WhatsApp)
│   └── accounts/        # Авторизация
│
├── static/              # Статические файлы
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/               # Загруженные файлы
│   └── products/
│
└── templates/           # HTML шаблоны
    ├── base.html
    ├── core/
    ├── catalog/
    ├── cart/
    └── accounts/
```

## 🛒 Функционал

### Каталог товаров
- ✅ Просмотр товаров по категориям (iPhone, Samsung, iPad, AirPods, Watch)
- ✅ Фильтрация по устройству, серии, дизайну
- ✅ Поиск товаров
- ✅ Детальная страница товара с изображениями

### Корзина (WhatsApp)
- ✅ Добавление товаров в корзину
- ✅ Просмотр корзины
- ✅ Оформление заказа через WhatsApp
- ✅ Сохранение корзины между сессиями

### Авторизация
- ✅ Регистрация пользователей
- ✅ Вход/выход
- ✅ Профиль пользователя

### Админ-панель
- ✅ Управление товарами
- ✅ Управление категориями
- ✅ Управление заказами (корзинами)
- ✅ Загрузка изображений

## 🔧 Админ-панель

1. **Войдите в админ-панель:**
   ```
   http://127.0.0.1:8000/admin/
   ```

2. **Используйте учетные данные суперпользователя**

3. **Добавьте товары через админку или используйте импорт:**
   ```bash
   python manage.py import_products
   ```

## 📊 Модели данных

### Product (Товар)
- `name` - Название
- `slug` - URL-идентификатор
- `device_type` - Тип устройства (iphone, samsung, etc.)
- `device_model` - Модель устройства
- `design_name` - Название дизайна (Sunset, Moonrise, etc.)
- `series` - Серия (Ultra-Slim, ProGuard, UltraGuard)
- `price` - Цена
- `sale_price` - Цена со скидкой
- `stock` - Остаток на складе
- `is_active` - Активен/не активен
- `is_new` - Новинка
- `is_featured` - Хит продаж

### Category (Категория)
- `name` - Название категории
- `slug` - URL-идентификатор

### Cart (Корзина)
- `session_key` - Ключ сессии
- `created_at` - Дата создания
- `updated_at` - Дата обновления

### CartItem (Элемент корзины)
- `cart` - Ссылка на корзину
- `product` - Ссылка на товар
- `quantity` - Количество

## 🎨 Дизайн

Сайт использует минималистичный дизайн в стиле PITAKA:
- Цветовая схема: черный, белый, серый
- Акцентный цвет: #25D366 (WhatsApp)
- Шрифты: системные (San Francisco, Segoe UI)

## 📱 WhatsApp Integration

При оформлении заказа создается сообщение вида:

```
Здравствуйте! Хочу заказать:

- iPhone 17 Pro Max (Sunset) - 1 шт. — 4 990 ₽
- iPhone 17 Pro (Moonrise) - 2 шт. — 9 980 ₽

Итого: 14 970 ₽
```

Клиент переходит в WhatsApp с уже заполненным сообщением.

## 🔐 Безопасность

- ✅ CSRF защита
- ✅ XSS защита
- ✅ Hash паролей
- ✅ Сессионные куки

## 🚀 Развертывание (Production)

### 1. Подготовьте проект

```bash
# Соберите статические файлы
python manage.py collectstatic

# Отключите debug режим
# В .env установите: DEBUG=False
```

### 2. Настройте веб-сервер

**Вариант A: Gunicorn + Nginx**

```bash
pip install gunicorn
gunicorn pitaka.wsgi:application --bind 0.0.0.0:8000
```

**Вариант B: WhiteNoise (простой вариант)**

Добавьте в `settings.py`:

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Добавьте это
    # ... остальные middleware
]
```

### 3. Рекомендуемые хостинги

- **Railway.app** - один клик для Django
- **Render.com** - бесплатный тариф
- **PythonAnywhere** - специализированный Python хостинг

## 📝 Команды управления

```bash
# Запуск сервера
python manage.py runserver

# Создание миграций
python manage.py makemigrations
python manage.py migrate

# Импорт товаров
python manage.py import_products

# Создание суперпользователя
python manage.py createsuperuser

# Сбор статики
python manage.py collectstatic

# Запуск тестов
python manage.py test
```

## 🐛 Решение проблем

### Ошибка "ModuleNotFoundError"
```bash
pip install -r requirements.txt
```

### Ошибка миграций
```bash
python manage.py migrate --run-syncdb
```

### Не работают статические файлы
```bash
python manage.py collectstatic --clear
```

### Ошибка базы данных
```bash
del db.sqlite3  # Windows
rm db.sqlite3   # macOS/Linux
python manage.py migrate
```

## 📞 Контакты

- WhatsApp: +7 (999) 123-45-67
- Email: info@pitaka.ru

## 📄 Лицензия

© 2025 PITAKA. Все права защищены.
