@echo off
echo ========================================
echo PITAKA Django Setup Script for Windows
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/6] Python found!
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo [2/6] Creating virtual environment...
    python -m venv venv
) else (
    echo [2/6] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo [3/6] Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Install dependencies
echo [4/6] Installing dependencies...
pip install -r requirements.txt
echo.

REM Run migrations
echo [5/6] Running database migrations...
python manage.py makemigrations
python manage.py migrate
echo.

REM Create superuser prompt
echo [6/6] Would you like to create a superuser (admin account)?
set /p CREATE_SUPER="Enter Y to create superuser, or N to skip: "
if /i "%CREATE_SUPER%"=="Y" (
    python manage.py createsuperuser
)
echo.

echo ========================================
echo Setup complete!
echo.
echo To run the development server:
echo   1. Run: venv\Scripts\activate
echo   2. Run: python manage.py runserver
echo   3. Open: http://127.0.0.1:8000
echo.
echo To import products:
echo   python manage.py import_products
echo ========================================
pause
