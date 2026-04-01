#!/bin/bash
echo "========================================"
echo "PITAKA Django Setup Script"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    exit 1
fi

echo "[1/6] Python found: $(python3 --version)"
echo ""

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "[2/6] Creating virtual environment..."
    python3 -m venv venv
else
    echo "[2/6] Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "[3/6] Activating virtual environment..."
source venv/bin/activate
echo ""

# Install dependencies
echo "[4/6] Installing dependencies..."
pip install -r requirements.txt
echo ""

# Run migrations
echo "[5/6] Running database migrations..."
python manage.py makemigrations
python manage.py migrate
echo ""

# Create superuser
echo "[6/6] Creating superuser..."
python manage.py createsuperuser
echo ""

echo "========================================"
echo "Setup complete!"
echo ""
echo "To run the development server:"
echo "  1. Run: source venv/bin/activate"
echo "  2. Run: python manage.py runserver"
echo "  3. Open: http://127.0.0.1:8000"
echo ""
echo "To import products:"
echo "  python manage.py import_products"
echo "========================================"
